import os
import argparse

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--paths", nargs="+", help="A list of paths to parse", required=True
    )

    print(parser.parse_args())

    args = vars(parser.parse_args())

    print(args)

    for path in args["paths"]:

        print(path)
