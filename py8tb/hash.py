"""
This script allows you to calculate the hash of a Video file
using the macOS and Linux utility shasum - a 256
"""

import time
import subprocess


def _subprocess_result_to_tuple(result):

    t_ = result.split(" ")

    if len(t_) > 2:
        hash = t_[0]
        path = " ".join(t_[1:])
        # quitamos el primer espacio y el \n (salto de línea final)
        path = path[1:-1]

    return (path, hash)


def file_to_hash(path) -> tuple:

    command = f"shasum -a 256 '{path}'"
    result = subprocess.check_output(command, shell=True, text=True)

    return _subprocess_result_to_tuple(result=result)


def apply_hast_to_list_of_paths(list_of_paths) -> list:

    r = []

    for path in list_of_paths:

        r.append(file_to_hash(path=path))
        time.sleep(0.5)

    return r
