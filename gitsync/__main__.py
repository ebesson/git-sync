import argparse
import gitsync.cli


def main():

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    gitsync.cli.main()


if __name__ == "__main__":
    main()