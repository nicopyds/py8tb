import numpy as np
import pandas as pd
import multiprocessing as mp

cores = mp.cpu_count()
photos = pd.read_parquet("photos.parquet.gzip").sample(700)["FilePath"].values.tolist()

splitted_photos = np.array_split(photos, indices_or_sections=cores - 1)
# PATHS = photos["FilePath"].sample(10).values.tolist()


def print_len_path(path):
    return len(path)


def get_len_path_splitted_photos(l):
    r = []
    for path_ in l:
        r.append((path_, len(path_)))
    return r


def main():
    pool = mp.Pool(processes=cores - 1)
    results = pool.map(func=get_len_path_splitted_photos, iterable=splitted_photos)
    pool.close()
    pool.join()

    # return pd.concat(results, axis=0)
    return results


if __name__ == "__main__":
    results = main()
