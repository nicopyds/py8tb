import os
from typing import Union
import pandas as pd
from py8tb.config import TOP_FILE_EXTENSIONS


def custom_mapping(file_extension):

    if str.lower(file_extension) in TOP_FILE_EXTENSIONS.keys():
        return TOP_FILE_EXTENSIONS[str.lower(file_extension)]
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
            f"Both df and path are None. You have to supply at least one of the params"
        )

    if path is not None:
        df = pd.read_parquet(path=path)

    df = add_custom_columns(df=df)

    df["CreationDate"] = pd.to_datetime(df["CreationDate"], format="%Y-%m-%d %H:%M:%S")
    df["LastModificationDate"] = pd.to_datetime(
        df["LastModificationDate"], format="%Y-%m-%d %H:%M:%S"
    )

    return df

def get_photos_df(df:Union[None, pd.DataFrame], path:Union[str, None]) -> pd.DataFrame:
    df = preprocessing_pipeline(df=df, path=path)
    photos = df[df["FileType"] == "photo"]
    return photos




