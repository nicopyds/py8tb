import os
import sys

import argparse

import pprint
from typing import Union

FILE_PATH = __file__
PY8TB_PATH = os.path.dirname(os.path.dirname(FILE_PATH))
SAVE_PATH = os.path.join(PY8TB_PATH, "data")

sys.path.insert(0, PY8TB_PATH)

from py8tb import Indexator


def main(folder_to_index: Union[list, str], save_path: str) -> None:

    indexator = Indexator(folder_to_index=folder_to_index)
    df = indexator.df
    pprint.pprint(df.head())
    indexator.save_df_to_parquet(save_path=save_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p", "--paths", nargs="+", help="A list of paths to parse", required=True
    )
    args = vars(parser.parse_args())

    FOLDER_TO_INDEX = args["paths"]

    main(folder_to_index=FOLDER_TO_INDEX, save_path=SAVE_PATH)
