import argparse
import sys

parser = argparse.ArgumentParser(prog="mxee", description="mxee", epilog="Making things easier.")
parser.add_argument("--bookmarks", action="store_true", help="test")
parser.add_argument("--test", action="store_true", help="test")


args = parser.parse_args()


if args.bookmarks:
    print("Die Tagersschau https://www.google.com")
    sys.exit(0)


if args.test:
    import mxee
    import mxee.helper
    import mxee.actions
    ws=mxee.config("main.workspace")
    mxee.actions.git_projects_status(ws)
    sys.exit(0)



