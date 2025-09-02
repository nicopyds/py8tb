import warnings

warnings.filterwarnings("ignore")

import argparse

from typing import Union

import numpy as np
import pandas as pd

import multiprocessing as mp


CORES = mp.cpu_count()


from py8tb import Indexator, parallel_ptb, get_photos_df, create_folder


def main(folder_to_index: Union[list, str], save_path: str) -> None:

    indexator = Indexator(folder_to_index=folder_to_index)
    df = indexator.df

    photos = get_photos_df(path=None, df=df)

    paths = photos["FilePath"]
    SPLITTED_PATHS = np.array_split(paths, CORES)

    pool = mp.Pool(processes=CORES)
    result_list = pool.map(func=parallel_ptb, iterable=SPLITTED_PATHS)

    pool.close()
    pool.join()

    result_dfs = map(
        lambda list_: pd.DataFrame(data=list_, columns=["FilePath", "Sha256"]),
        result_list,
    )
    result_dfs = list(result_dfs)

    photos = pd.concat(result_dfs, axis=0)

    df = pd.merge(left=df, right=photos, on="FilePath", how="left")
    indexator.df = df
    create_folder(path=save_path)
    indexator.save_df_to_parquet(save_path=save_path)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path_to_index",
        nargs="+",
        help="A list of paths to parse",
        required=True,
    )
    parser.add_argument(
        "-s", "--path_to_save", help="Path where to save the file", required=True
    )
    args = vars(parser.parse_args())

    FOLDER_TO_INDEX = args["path_to_index"]
    SAVE_PATH = args["path_to_save"]

    main(folder_to_index=FOLDER_TO_INDEX, save_path=SAVE_PATH)
