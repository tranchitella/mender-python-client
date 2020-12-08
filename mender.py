import argparse
import logging as log
import sys

import src.statemachine.statemachine as statemachine
import src.bootstrap as bootstrap

def run_daemon(args):
    print("Running daemon...")
    statemachine.StateMachine().run()
    print(args)

def show_artifact(args):
    print("Showing Artifact:")
    print(args)

def run_bootstrap(args):
    print("Bootstrapping...")
    print(args)
    a = bootstrap.now()
    print(type(a))
    log.info("Device bootstrapped successfully")

def main():
    # TODO -- set up logging properly
    # For now, only write to the tty
    log.basicConfig(stream=sys.stderr, level=log.DEBUG)
    log.info("Hello, world!")
    parser = argparse.ArgumentParser(
        prog="mender",
        description="""mender
    integrates both the mender daemon and commands for manually performing
    tasks performed by the daemon (see list of COMMANDS below).""",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    #
    # Commands
    #
    subcommand_parser = parser.add_subparsers(title="COMMANDS")
    # TODO -- Needs the --forcebootstrap flag
    bootstrap_parser = subcommand_parser.add_parser(
        "bootstrap", help="Perform bootstrap and exit."
    )
    bootstrap_parser.add_argument(
        "--forcebootstrap", "-F", help="Force bootstrap.", type=bool, default=False
    )
    bootstrap_parser.set_defaults(func=run_bootstrap)
    daemon_parser = subcommand_parser.add_parser(
        "daemon", help="Start the client as a background service."
    )
    daemon_parser.set_defaults(func=run_daemon)
    show_artifact_parser = subcommand_parser.add_parser(
        "show-artifact",
        help="Print the current Artifact name to the command line and exit.",
    )
    show_artifact_parser.set_defaults(func=show_artifact)
    #
    # Options
    #
    global_options = parser.add_argument_group("GLOBAL OPTIONS")
    global_options.add_argument(
        "--config",
        "-c",
        help="Configuration FILE path.",
        default="/etc/mender/mender.conf",
    )
    global_options.add_argument(
        "--fallback-config",
        "-b",
        help="Fallback configuration FILE path.",
        default="/var/lib/mender/mender.conf",
    )
    global_options.add_argument(
        "--data",
        "-d",
        help="Mender state data DIRECTORY path.",
        default="/var/lib/mender",
    )
    # Logging setup
    global_options.add_argument(
        "--log-file", "-L", help="FILE to log to.", default="syslog", metavar="FILE"
    )
    global_options.add_argument(
        "--log-level", "-l", help="Set logging to level.", default="info"
    )
    global_options.add_argument(
        "--trusted-certs",
        "-E",
        help="Truster server certificates FILE path.",
        default="system certificates",
    )
    global_options.add_argument(
        "--forcebootstrap", "-F", help="Force bootstrap.", type=bool, default=False
    )
    global_options.add_argument(
        "--no-syslog", help="Disble logging to syslog.", type=bool, default=False
    )
    global_options.add_argument(
        "--skipverify", help="Skip certificate verification.", type=bool, default=False
    )
    global_options.add_argument(
        "--version", "-v", help="print the version", type=bool, default=False
    )
    # statemachine.StateMachine().run()
    args = parser.parse_args()
    print(vars(args))
    print(args)
    args.func(args)
    # if args.bootstrap:
    #     print("Bootstrapping...")
    # if args.daemon:
    #     print("Starting the Mender-client daemon...")
    # if args.show_artifact:
    #     print("Artifact: foobar")
    # parser.print_help()



if __name__ == "__main__":
    main()
