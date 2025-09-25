import os
import shutil
import pandas as pd
import matplotlib.pyplot as plt


def create_outer_folder():
    file_path = os.path.abspath(__file__)
    file_path = os.path.dirname(file_path)

    testing_folder = os.path.join(file_path, "folder_with_data")

    if os.path.isdir(testing_folder):
        shutil.rmtree(testing_folder)

    os.makedirs(testing_folder)

    return testing_folder


def create_inner_folder():
    outer_folder = create_outer_folder()

    inner_folders = [
        os.path.join(outer_folder, "caso1"),
        os.path.join(outer_folder, "caso2_1"),
        os.path.join(outer_folder, "caso2_2"),
        os.path.join(outer_folder, "caso3_1"),
        os.path.join(outer_folder, "caso3_2"),
    ]

    for inner_folder_ in inner_folders:
        os.makedirs(inner_folder_)

    return inner_folders


def get_dummy_df():
    dummy_data = {"index": [1, 2, 3, 4, 5], "data": [6, 7, 8, 9, 10]}
    dummy_df = pd.DataFrame(data=dummy_data)
    return dummy_df


def generate_random_figures(show=False):
    df = get_dummy_df()
    inner_folders = create_inner_folder()

    fig = plt.figure()
    ax = fig.subplots()
    ax.plot(df)

    if show:
        plt.show()

    # caso 1: la misma foto en la misma carpeta con 2 nombres diferentes
    plt.savefig(os.path.join(inner_folders[0], "photo1.png"))
    plt.savefig(os.path.join(inner_folders[0], "photo2.png"))

    # caso 2: la misma foto en 2 carpetas diferentes con el mismo nombre
    plt.savefig(os.path.join(inner_folders[1], "photo3.png"))
    plt.savefig(os.path.join(inner_folders[2], "photo3.png"))

    # caso 3: la misma foto en 2 carpetas diferentes con el diferente nombre
    plt.savefig(os.path.join(inner_folders[3], "photo4.png"))
    plt.savefig(os.path.join(inner_folders[4], "photo5.png"))


def main():
    generate_random_figures()


if __name__ == "__main__":
    main()
