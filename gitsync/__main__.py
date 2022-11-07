import argparse
import gitsync.cli
import ptvsd
import time


def main():

    parser = argparse.ArgumentParser()
    args = parser.parse_args()

    gitsync.cli.main()


if __name__ == "__main__":
    main()