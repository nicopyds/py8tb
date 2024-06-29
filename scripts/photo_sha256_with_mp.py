import os
import sys

import numpy as np
import pandas as pd
import multiprocessing as mp

CORES = mp.cpu_count()

FILE_PATH = __file__
PY8TB_PATH = os.path.dirname(os.path.dirname(FILE_PATH))
SAVE_PATH = os.path.join(PY8TB_PATH, "data")

PHOTOS = pd.read_parquet(os.path.join(SAVE_PATH, "photos.parquet.gzip"))
PATHS = PHOTOS["FilePath"].sample(50).values.tolist()
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
    results = main()
    print(len(results))
    print(results[0][:100])
