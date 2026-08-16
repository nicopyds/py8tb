from os import rename
from pathlib import Path
from datetime import datetime
import subprocess
import json
import re
import multiprocessing as mp

import numpy as np
import pandas as pd


def rename_file(old_path: str, new_path: str) -> str:
    """
    Renames a file from old_path to new_path.

    Raises:
        FileNotFoundError:
            Source file does not exist.

        FileExistsError:
            Destination file already exists.

    Returns:
        New path as string.
    """

    old_path = Path(old_path)
    new_path = Path(new_path)

    if not old_path.exists():
        raise FileNotFoundError(f"Source file does not exist: {old_path}")

    if new_path.exists():
        raise FileExistsError(f"Destination file already exists: {new_path}")

    old_path.rename(new_path)

    return str(new_path)


if __name__ == "__main__":

    path = "/Users/nicolaepopescul/code/streams/py8tb/scripts/df_full.xlsx"

    df = pd.read_excel(path)
    print(df.isnull().sum())
    print(df.shape)
    df = df.dropna()
    df = df[["FilePath", "NewPath"]]
    print(df.shape)
    print(df.head())
    
    old_paths = df["FilePath"].tolist()
    new_paths = df["NewPath"].tolist()

    for old_path, new_path in zip(old_paths, new_paths):
        rename_file(old_path=old_path, new_path=new_path)

