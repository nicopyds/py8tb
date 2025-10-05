import os
import pandas as pd
from py8tb.config import TOP_FILE_EXTENSIONS


def custom_mapping(file_extension):

    # TODO
    # when working on MacOS, if the file is .DS_Store
    # you will get NA
    if str.lower(file_extension) in TOP_FILE_EXTENSIONS.keys():
        return TOP_FILE_EXTENSIONS[str.lower(file_extension)]
    elif file_extension == ".DS_Store":
        return "mac_file_organizer"
    else:
        return "na"


def add_custom_columns(df):

    df = df.assign(
        FileName=df["FilePath"].apply(os.path.basename),
        FileExtension=df["FilePath"].apply(
            lambda file_path: str.lower(os.path.splitext(file_path)[1])
        ),
        FileType=lambda df: df["FileExtension"].apply(custom_mapping),
    )

    return df


def preprocessing_pipeline(df=None, path=None):

    if df is None and path is None:
        raise Exception(
            "Both df and path are None. You have to supply at least one of the params"
        )

    if path is not None:
        df = pd.read_parquet(path=path)

    df = add_custom_columns(df=df)

    df["CreationDate"] = pd.to_datetime(df["CreationDate"], format="%Y-%m-%d %H:%M:%S")
    df["LastModificationDate"] = pd.to_datetime(
        df["LastModificationDate"], format="%Y-%m-%d %H:%M:%S"
    )

    return df
