"""
This script allows you to calculate the hash of a Video file
using the macOS and Linux utility shasum - a 256
"""

import subprocess


def _subprocess_result_to_tuple(result):

    t_ = result.split(" ")

    if len(t_) > 2:
        hash = t_[0]
        path = " ".join(t_[1:])

    return (path, hash)


def video_to_hash(path) -> tuple:

    command = f"shasum -a 256 '{path}'"
    result = subprocess.check_output(command, shell=True, text=True)

    return _subprocess_result_to_tuple(result=result)


def video_to_hash_list(splited_paths):
    return [video_to_hash(path=path_) for path_ in splited_paths]
