import time
import logging as log

import src.inventory.aggregator as inventory
import src.identity.aggregator as identity
import src.bootstrap as bootstrap
import src.client.authorize as authorize
import src.config.config as config

# TODO -- How to construct the context (?)
class Context(object):
    """Class for storing the state-machine context"""

    def __init__(self):
        self.private_key = None


class State(object):
    def __init__(self):
        pass

    # TODO -- needed or not (?)
    def pre(self):
        pass

    # TODO -- needed or not (?)
    def post(self):
        pass

    def run(self):
        pass


class Init(State):
    def run(self, context):
        log.debug("InitState: run()")
        try:
            context.config = {}
            config_file = config.load(
                local_path="tests/data/configs/local_mender.conf",
                global_path="tests/data/configs/global_mender.conf",
            )
            context.config = config_file
            log.info(f"Loaded configuration: {config_file}")
        except config.NoConfigurationFileError:
            log.error(
                "No configuration files found for the device."
                "Most likely, the device will not be functional."
            )
        identity_data = identity.aggregate(
            path="tests/data/identity/mender-device-identity"
        )
        context.identity_data = identity_data
        private_key = bootstrap.now()
        context.private_key = private_key
        context.foo = "bar"
        log.debug(f"Init set context to: {context}")
        return context


##########################################


def run():
    StateMachine().run()


class StateMachine(object):

    # Maybe hold the context here (?)

    def __init__(self):
        log.info("Initializing the state-machine")
        self.context = Context()
        self.context.private_key = "foo"
        log.info(f"ctx: {self.context}")
        self.unauthorized_machine = UnauthorizedStateMachine()
        self.authorized_machine = AuthorizedStateMachine()

    def run(self):
        self.context = Init().run(self.context)
        log.debug(f"Initialized context: {self.context}")
        while True:
            self.unauthorized_machine.run(self.context)
            self.authorized_machine.run()


#
# Hierarchical - Yes!
#
# i.e., Authorized, and Unauthorized state-machine
#


class Authorize(State):
    def run(self, context):
        log.info("Authorizing...")
        log.debug(f"Current context: {context}")
        time.sleep(3)
        authorize.request(
            context.config.ServerURL,
            context.config.TenantToken,
            context.identity_data,
            context.private_key,
        )
        return True


class Idle(State):
    def run(self, context):
        print("Idling...")
        time.sleep(10)
        return True


class UnauthorizedStateMachine(StateMachine):
    """Handle Wait, and Authorize attempts"""

    def __init__(self):
        pass

    def run(self, context):
        while True:
            if Authorize().run(context):
                return
            Idle().run(context)


class AuthorizedStateMachine(StateMachine):
    """Handle Inventory update, and update check"""

    def __init__(self):
        self.authorized = True  # TODO -- Set this to 'False'
        self.idle_machine = IdleStateMachine()
        self.update_machine = UpdateStateMachine()

    def run(self):
        while self.authorized:
            self.idle_machine.run()  # Idle returns when an update is ready
            UpdateStateMachine().run()  # Update machine runs when idle detects an update


# Should transitions always go through the external state-machine, to verify and
# catch de-authorizations (?)
#
# Second layered machine (below Authorized)
#
# Idling - Or, just pushing inventory and identity data and looking for updates


class SyncInventory(State):
    def run(self):
        print("Syncing the inventory...")
        vals = inventory.aggregate(path="./tests/data/inventory/")
        print(f"aggreated inventory data: {vals}")
        time.sleep(1)


class SyncUpdate(State):
    def run(self):
        print("Checking for updates...")
        time.sleep(2)
        return True


class IdleStateMachine(AuthorizedStateMachine):
    def __init__(self):
        pass

    def run(self):
        while True:
            SyncInventory().run()
            if SyncUpdate().run():
                return


#
# Updating - Run the update state-machine
#

# TODO -- should it have a separate state-machine for the 'dirty' partition ?

# This will be the most advanced setup, by far !


class Download(State):
    def run(self):
        print("Running the Download state...")
        return ArtifactInstall()


class ArtifactInstall(State):
    def run(self):
        print("Running the ArtifactInstall state...")
        return ArtifactReboot()


class ArtifactInstall(State):
    def run(self):
        print("Running the ArtifactInstall state...")
        return ArtifactReboot()


class ArtifactReboot(State):
    def run(self):
        print("Running the ArtifactReboot state...")
        return ArtifactCommit()


class ArtifactCommit(State):
    def run(self):
        print("Running the ArtifactCommit state...")
        return ArtifactRollback()


class ArtifactRollback(State):
    def run(self):
        print("Running the ArtifactRollback state...")
        return ArtifactRollbackReboot()


class ArtifactRollbackReboot(State):
    def run(self):
        print("Running the ArtifactRollbackReboot state...")
        return ArtifactFailure()


class ArtifactFailure(State):
    def run(self):
        print("Running the ArtifactFailure state...")
        return _UpdateDone()


class _UpdateDone(State):
    def __str__(self):
        return "done"

    def __eq__(self, other):
        return isinstance(other, _UpdateDone)

    def run(self):
        assert False


# The update state-machine is the most advanced machine we need
class UpdateStateMachine(AuthorizedStateMachine):
    def __init__(self):
        self.current_state = Download()

    def run(self):
        while self.current_state != _UpdateDone():
            self.current_state = self.current_state.run()
            time.sleep(1)
