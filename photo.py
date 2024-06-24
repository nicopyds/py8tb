import datetime

from typing import Union
from hashlib import sha256

import numpy as np
import pandas as pd
import multiprocessing as mp

cores = mp.cpu_count()
photos = pd.read_parquet("photos.parquet.gzip")

PATHS = photos["FilePath"].sample(100).values.tolist()
SPLITTED_PATHS = np.array_split(ary = PATHS, indices_or_sections = cores) # 10_000/8


class PhotoToBytes:

    def __init__(self, path: list) -> None:
        self.path = path

    def open_contents(self, path):

        try:
            with open(path, "rb") as f:
                contents = f.read()
                return contents
        except:
            raise Exception(f"Mira bien porque ha fallado {path}")

    def content_to_bytes(self, path):

        return bytearray(self.open_contents(path=path))

    def create_sha256(self):

        l = []

        for i, path_ in enumerate(self.path):
            hash_file = sha256(string=self.content_to_bytes(path=path_)).hexdigest()
            t = (path_, hash_file)
            l.append(t)

        return l


def parallel_ptb(splitted_paths):
    ptb = PhotoToBytes(path = splitted_paths)
    return ptb.create_sha256()


def main():
    pool = mp.Pool(processes = cores)
    results = pool.map(func = parallel_ptb, iterable = SPLITTED_PATHS)
    pool.close()
    pool.join()
    return results


if __name__ == "__main__":
    results = main()
    print(len(results))
    print(results[0][:100])
