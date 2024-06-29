import os
import pprint
from typing import Union

import pandas as pd

from .utils import (
    get_file_creation_date,
    get_file_modification_date,
    get_file_size_mb,
    get_watermark,
)


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
        save_path_filename = os.path.join(save_path, f"df_{get_watermark()}.xlsx")

        df_.to_excel(excel_writer=save_path_filename)

    def save_df_to_parquet(self, save_path: str) -> None:

        df_ = self.df
        save_path_filename = os.path.join(
            save_path, f"df_{get_watermark()}.parquet.gzip"
        )

        df_.to_parquet(path=save_path_filename)
