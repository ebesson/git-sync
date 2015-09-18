import sys
from gitsync import GitSync


def main():
    try:
        GitSync().sync_all()
    except KeyboardInterrupt:
        print("... terminating git-sync")
        sys.exit(130)
    except Exception as e:
        print(str(e))
        sys.exit(1)

if __name__ == "__main__":
    main()
