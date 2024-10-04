import os
import datetime

def create_folder(path):
    if not os.path.isdir(path):
        os.makedirs(path)

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
    return os.stat(file_path).st_size / (1024 * 1024)
