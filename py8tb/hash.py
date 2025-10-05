"""
This script allows you to calculate the hash of a Video file
using the macOS and Linux utility shasum - a 256
"""

import subprocess
import numpy as np


def _subprocess_result_to_tuple(result):

    t_ = result.split(" ")

    if len(t_) > 2:
        hash = t_[0]
        path = " ".join(t_[1:])
        # quitamos el primer espacio y el \n (salto de línea final)
        path = path[1:-1]

    return (path, hash)


def file_to_hash(path) -> tuple:

    random_value = np.random.rand()
    command = f"shasum -a 256 '{path}'"

    if random_value < 0.01:
        print("Working with this command")
        print(command)

    try:
        result = subprocess.check_output(command, shell=True, text=True)
        result = _subprocess_result_to_tuple(result=result)

        return result

    except Exception as e:
        return (path, e)


def apply_hast_to_list_of_paths(list_of_paths) -> list:

    r = []

    for path in list_of_paths:

        r.append(file_to_hash(path=path))

    return r
