import pprint
import os
from typing import Union
import datetime

import pandas as pd


def get_watermark():

    str_now = str(datetime.datetime.now())

    year_month_day = str_now.split(" ")[0].replace("-", "_")
    hour_minutes_seconds = str_now.split(" ")[1][:8].replace(":", "_")

    return "_".join([year_month_day, hour_minutes_seconds])


def unix_to_date_converter(ut: float) -> str:
    return datetime.datetime.fromtimestamp(timestamp=ut).strftime("%Y-%m-%d %H:%M:%S")


def get_file_creation_date(file_path: str, return_date: bool = True) -> float:

    ut = os.path.getctime(file_path)

    if return_date:
        return unix_to_date_converter(ut=ut)
    else:
        return ut


def get_file_modification_date(file_path: str, return_date: bool = True) -> float:

    ut = os.path.getmtime(file_path)

    if return_date:
        return unix_to_date_converter(ut=ut)
    else:
        return ut


def get_file_size_mb(file_path: str) -> float:
    # return in mb
    return os.stat(file_path).st_size / (1024 * 1024)


class Indexator:

    def __init__(self, folder_to_index: Union[list, str]) -> None:

        self.__assert_folder_to_index(folder_to_index=folder_to_index)
        folder_to_index = self.__check_if_folder_to_index_is_list(
            folder_to_index=folder_to_index
        )

        self.folder_to_index = folder_to_index

    def __assert_folder_to_index(self, folder_to_index: Union[list, str]) -> None:

        assert_message = f"folder_to_index must be a list or str, you have passed {type(folder_to_index)}"
        assert isinstance(folder_to_index, (list, str)), assert_message

    def __check_if_folder_to_index_is_list(
        self, folder_to_index: Union[list, str]
    ) -> list:

        if isinstance(folder_to_index, str):
            folder_to_index = [folder_to_index]

        return folder_to_index

    def index_folders(self) -> list:

        indexed_files = []

        for full_dir in self.folder_to_index:
            for full_dir, subdirs, file_names in os.walk(full_dir):
                for file_name in file_names:
                    file_path = os.path.join(full_dir, file_name)

                    file_creation_date = get_file_creation_date(file_path=file_path)
                    file_modification_date = get_file_modification_date(
                        file_path=file_path
                    )

                    file_size_mb = get_file_size_mb(file_path=file_path)

                    indexed_files.append(
                        (
                            file_path,
                            file_creation_date,
                            file_modification_date,
                            file_size_mb,
                        )
                    )

        return indexed_files

    def __indexed_files_to_df(self) -> pd.DataFrame:

        indexed_files = self.index_folders()
        columns = ["FilePath", "CreationDate", "LastModificationDate", "SizeMB"]

        df = pd.DataFrame(data=indexed_files, columns=columns)

        return df

    @property
    def df(self) -> pd.DataFrame:

        if not hasattr(self, "_df"):
            self._df = self.__indexed_files_to_df()

        df_ = self._df.copy(deep=True)

        return df_

    def save_df_to_excel(self, save_path: str) -> None:

        df_ = self.df

        df_.to_excel(excel_writer=save_path)

    def save_df_to_parquet(self, save_path: str) -> None:

        df_ = self.df

        df_.to_parquet(path=save_path)


def main(folder_to_index: Union[list, str], save_path: str) -> None:

    indexator = Indexator(folder_to_index=folder_to_index)
    df = indexator.df
    pprint.pprint(df.head())
    indexator.save_df_to_parquet(save_path=save_path)


if __name__ == "__main__":

    CWD = os.getcwd()
    SAVE_PATH = os.path.join(CWD, f"df_{get_watermark()}.parquet.gzip")

    FOLDER_TO_INDEX = ["/Volumes/MUPU 4TB 1", "/Volumes/MUPU 4TB 2"]

    main(folder_to_index=FOLDER_TO_INDEX, save_path=SAVE_PATH)
