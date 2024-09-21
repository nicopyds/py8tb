import argparse

import pprint
from typing import Union

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
    parser.add_argument(
        "-s", "--save_path",  help="Path where to save the file", required=True
    )
    args = vars(parser.parse_args())

    FOLDER_TO_INDEX = args["paths"]
    SAVE_PATH = args["save_path"]
    main(folder_to_index=FOLDER_TO_INDEX, save_path=SAVE_PATH)
