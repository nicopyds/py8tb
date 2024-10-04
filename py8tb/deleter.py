import os

import pprint

import argparse

import pandas as pd
from py8tb import get_photos_df

class FileDeleter():

    def __init__(self, path:str) -> None:
        self.path = path
        self.___load_df()
        
        
    def ___load_df(self):
        self.df = get_photos_df(df = None, path=self.path)

    def report(self):
        total_photos = self.df["FileType"].value_counts().iloc[0]
        unique_photos = self.df.groupby(["Sha256"]).size().size

        duplicates_photos = total_photos - unique_photos
        
        print(f"We have found a total of {duplicates_photos}")


    def get_path_to_delete(self) -> dict:


        sha256_list = self.df["Sha256"].values.tolist()
        path_list = self.df["FilePath"].values.tolist()


        dict_sha256_to_save = {}
        dict_sha256_to_delete = {}

        for sha256_, path_ in zip(sha256_list, path_list):
            if sha256_ not in dict_sha256_to_save.keys():
                dict_sha256_to_save[sha256_] = path_
            else:
                dict_sha256_to_delete[path_] = sha256_

        return dict_sha256_to_delete

    def delete_files(self, execute:bool = False) -> None:
        paths_to_delete = list(self.get_path_to_delete().keys())

        if execute:
            for path_to_delete in paths_to_delete:
                os.remove(path=path_to_delete)


if __name__ == "__main__":

    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-p",
        "--path_to_df",
        nargs="+",
        help="The path to the df indexed and with sha256 for each file",
        required=True,
    )

    parser.add_argument(
        "-e",
        "--execute",
        help="Flag to confirm the deletion of the files",
        action=argparse.BooleanOptionalAction,
        required=False,
        default=False,
        type=bool
    )


    args = vars(parser.parse_args())

    PATH_TO_DF = args["path_to_df"]
    EXECUTE = args["execute"]
    
    print(type(EXECUTE))
    print(EXECUTE)


    fd = FileDeleter(path=PATH_TO_DF)
    fd.report()
    files_to_delete = fd.get_path_to_delete()

    pprint.pprint(files_to_delete)
    fd.delete_files(execute = EXECUTE)


