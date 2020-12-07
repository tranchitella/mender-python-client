import time

import src.inventory.aggregator as inventory


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
    def run(self):
        pass


##########################################

def run():
    StateMachine().run()


class StateMachine(object):
    def __init__(self):
        self.unauthorized_machine = UnauthorizedStateMachine()
        self.authorized_machine = AuthorizedStateMachine()

    def run(self):
        Init().run()
        while True:
            self.unauthorized_machine.run()
            self.authorized_machine.run()


#
# Hierarchical - Yes!
#
# i.e., Authorized, and Unauthorized state-machine
#


class Authorize(State):
    def run(self):
        print("Authorizing...")
        time.sleep(3)
        return True


class Idle(State):
    def run(self):
        print("Idling...")
        time.sleep(10)
        return True


class UnauthorizedStateMachine(StateMachine):
    """Handle Wait, and Authorize attempts"""

    def __init__(self):
        pass

    def run(self):
        while True:
            if Authorize().run():
                return
            Idle().run()


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
