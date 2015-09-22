from gitsync import GitSync
from termcolor import cprint
import sys


def main():
    try:
        GitSync().sync_all()
    except KeyboardInterrupt:
        cprint("... terminating git-sync", "green")
        sys.exit(130)
    except Exception as e:
        cprint(text=str(e), color='red', attrs=['bold'])
        sys.exit(1)

if __name__ == "__main__":
    main()
