import os
import sys

import datetime
import pickle
import numpy as np
import pandas as pd
import multiprocessing as mp

# SAMPLE = 10_000
CORES = mp.cpu_count()

FILE_PATH = __file__
PY8TB_PATH = os.path.dirname(os.path.dirname(FILE_PATH))
SAVE_PATH = os.path.join(PY8TB_PATH, "data")

PHOTOS = pd.read_parquet(os.path.join(SAVE_PATH, "photos.parquet.gzip"))
# PATHS = PHOTOS["FilePath"].sample(SAMPLE).values.tolist()
PATHS = PHOTOS["FilePath"].values.tolist()

SPLITTED_PATHS = np.array_split(ary=PATHS, indices_or_sections=CORES)

sys.path.insert(0, PY8TB_PATH)

from py8tb import parallel_ptb


def main():
    pool = mp.Pool(processes=CORES)
    result_list = pool.map(func=parallel_ptb, iterable=SPLITTED_PATHS)
    pool.close()
    pool.join()
    return result_list


if __name__ == "__main__":

    print(len(PATHS))

    st = datetime.datetime.now()

    results = main()
    results = sum(results, [])
    print(len(results))

    with open(os.path.join(SAVE_PATH, "photos_sha256.pkl"), "wb") as f:
        pickle.dump(results, f)

    et = datetime.datetime.now()
    tt = et - st
    # print(f"Total time took {tt} in seconds for {SAMPLE} samples!")
    print(f"Total time took {tt} in seconds!")
