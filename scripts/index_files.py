import warnings

warnings.filterwarnings("ignore")

import os
import argparse

from typing import Union

import numpy as np
import pandas as pd

import multiprocessing as mp

CORES = mp.cpu_count()

FILE_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(FILE_PATH)

from py8tb import (
    Indexator,
    create_folder,
    apply_hast_to_list_of_paths,
    preprocessing_pipeline,
    get_watermark,
)


def main(folder_to_index: Union[list, str], save_path: str) -> None:

    # We index all the files from the specified folder_to_index
    indexator = Indexator(folder_to_index=folder_to_index)

    df = indexator.df
    df = preprocessing_pipeline(df=df)

    print("Indexed all the folders and saved a temporary csv file")

    # createa a unique watermark to save files from the same
    # script execution
    watermark = get_watermark()

    file_name_df = f"df_{watermark}.csv"
    df.to_csv(os.path.join(save_path, file_name_df), index=False)

    paths = df["FilePath"]

    SPLITTED_PATHS = np.array_split(paths, CORES)

    pool = mp.Pool(processes=CORES)

    result_list = pool.map(func=apply_hast_to_list_of_paths, iterable=SPLITTED_PATHS)

    pool.close()
    pool.join()

    # fmt: off
    result_dfs = pd.concat(list(map(lambda list_: pd.DataFrame(data=list_, columns=["FilePath", "Sha256"]), result_list)), axis = 0)
    # fmt: on

    file_name_results = f"results_dfs_{watermark}.csv"
    result_dfs.to_csv(os.path.join(save_path, file_name_results), index=False)

    merged = pd.merge(left=df, right=result_dfs, on="FilePath", how="left")

    create_folder(path=save_path)

    file_name_csv = f"merged_{watermark}.csv"
    merged.to_csv(os.path.join(save_path, file_name_csv), index=False)


if __name__ == "__main__":

    # fmt: off
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path_to_index",
        nargs="+",
        help="A list of paths to parse",
        required=False,
    )
    parser.add_argument(
        "-s",
        "--path_to_save",
        help="Path where to save the file",
        required=False
    )
    args = vars(parser.parse_args())

    # testing values

    FOLDER_TO_INDEX_TEST = os.path.join(os.path.dirname(DIR_PATH), "real_data")
    SAVE_PATH_TEST = os.path.join(os.path.dirname(DIR_PATH), "data")

    # fmt: on

    FOLDER_TO_INDEX = args.get("path_to_index", FOLDER_TO_INDEX_TEST)

    SAVE_PATH = (
        args["path_to_save"] if args["path_to_save"] is not None else SAVE_PATH_TEST
    )

    print(FOLDER_TO_INDEX)
    print(SAVE_PATH)

    main(folder_to_index=FOLDER_TO_INDEX, save_path=SAVE_PATH)
