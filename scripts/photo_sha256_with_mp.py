import argparse
import os

import numpy as np
import pandas as pd
import multiprocessing as mp

from py8tb import parallel_ptb, get_photos_df

CORES = mp.cpu_count()


def main(photo_df):

    photos = get_photos_df(path=photo_df, df=None)

    paths = photos["FilePath"]
    SPLITTED_PATHS = np.array_split(paths, CORES)

    pool = mp.Pool(processes=CORES)
    result_list = pool.map(func=parallel_ptb, iterable=SPLITTED_PATHS)

    pool.close()
    pool.join()

    return result_list


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument("-p", "--path", help="Path to the photo df", required=True)
    parser.add_argument(
        "-s", "--save_path", help="Path where to save the file", required=True
    )
    args = vars(parser.parse_args())

    PHOTO_DF = args["path"]
    SAVE_PATH = args["save_path"]

    result_list = main(PHOTO_DF)
    result_dfs = map(
        lambda list_: pd.DataFrame(data=list_, columns=["FilePath", "Sha256"]),
        result_list,
    )
    result_dfs = list(result_dfs)

    photos = pd.concat(result_dfs, axis=1)
    photos.to_parquet(os.path.join(SAVE_PATH, "sha256.parquet.gzip"))
