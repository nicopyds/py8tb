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

    indexator = Indexator(folder_to_index=folder_to_index)
    df = indexator.df
    df = preprocessing_pipeline(df=df)

    paths = df[df["FileType"].isin(["photo", "video"])]["FilePath"]

    SPLITTED_PATHS = np.array_split(paths, CORES)

    pool = mp.Pool(processes=CORES)

    result_list = pool.map(func=apply_hast_to_list_of_paths, iterable=SPLITTED_PATHS)

    pool.close()
    pool.join()

    # fmt: off
    result_dfs = pd.concat(list(map(lambda list_: pd.DataFrame(data=list_, columns=["FilePath", "Sha256"]), result_list)), axis = 0)
    # fmt: on

    df = pd.merge(left=df, right=result_dfs, on="FilePath", how="left")

    create_folder(path=save_path)
    watermark = get_watermark()

    file_name_csv = f"df_{watermark}.csv"
    df.to_csv(os.path.join(save_path, file_name_csv), index=False)

    # results_df_csv = f"results_df{watermark}.csv"
    # result_dfs.to_csv(os.path.join(save_path, results_df_csv), index=False)


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

    # FOLDER_TO_INDEX = args["path_to_index"]
    # SAVE_PATH = args["path_to_save"]

    # fmt: on

    FOLDER_TO_INDEX_ = os.path.join(os.path.dirname(DIR_PATH), "real_data")
    SAVE_PATH_ = os.path.join(os.path.dirname(DIR_PATH), "data")

    FOLDER_TO_INDEX = args.get("--path_to_index", FOLDER_TO_INDEX_)
    SAVE_PATH = args.get("__path_to_save", SAVE_PATH_)

    print(FOLDER_TO_INDEX)
    print(SAVE_PATH)

    main(folder_to_index=FOLDER_TO_INDEX, save_path=SAVE_PATH)
