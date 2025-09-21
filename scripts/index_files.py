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
    PhotoToBytes,
    parallel_ptb,
    get_photos_df,
    create_folder,
    video_to_hash,
    video_to_hash_list,
    preprocessing_pipeline,
)


def apply_file_to_hash(df: pd.DataFrame):

    r = []

    for row in df.iterrows():

        path = row["FilePath"]
        file_type = row["FileType"]

        if file_type == "photo":
            r.append(PhotoToBytes.content_to_bytes(path=path))

        elif file_type == "video":
            r.append(video_to_hash(path=path))

    return r


def main(folder_to_index: Union[list, str], save_path: str) -> None:

    indexator = Indexator(folder_to_index=folder_to_index)
    df = indexator.df
    df = preprocessing_pipeline(df=df)

    paths = df[df["FileType"].isin(["photo", "video"])]["FilePath"]
    # paths = df[df["FileType"].isin(["video"])]["FilePath"]
    # paths = df[df["FileType"].isin(["photo"])]["FilePath"]
    print(len(paths))
    SPLITTED_PATHS = np.array_split(paths, CORES)

    pool = mp.Pool(processes=CORES)

    # result_list = pool.map(func=parallel_ptb, iterable=SPLITTED_PATHS)

    result_list = pool.map(func=video_to_hash_list, iterable=SPLITTED_PATHS)

    # result_list = pool.map(func=apply_file_to_hash, iterable=SPLITTED_PATHS)

    pool.close()
    pool.join()

    print(result_list)
    print(len(result_list))


#
##result_dfs = map(
# lambda list_: pd.DataFrame(data=list_, columns=["FilePath", "Sha256"]),
# result_list,
# )
# result_dfs = list(result_dfs)
#
# photos = pd.concat(result_dfs, axis=0)
#
# df = pd.merge(left=df, right=photos, on="FilePath", how="left")
# indexator.df = df
# create_folder(path=save_path)
# indexator.save_df_to_parquet(save_path=save_path)
#
#
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

    #FOLDER_TO_INDEX = args["path_to_index"]
    #SAVE_PATH = args["path_to_save"]

    #fmt: off

    FOLDER_TO_INDEX_ = os.path.join(os.path.dirname(DIR_PATH), "real_data")
    SAVE_PATH_ = os.path.join(os.path.dirname(DIR_PATH), "data")

    FOLDER_TO_INDEX = args.get("--path_to_index", FOLDER_TO_INDEX_)
    SAVE_PATH = args.get("__path_to_save", SAVE_PATH_)

    print(FOLDER_TO_INDEX)
    print(SAVE_PATH)

    main(folder_to_index=FOLDER_TO_INDEX, save_path=SAVE_PATH)
