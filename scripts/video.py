import os
from py8tb import video_to_hash

FILE_PATH = os.path.abspath(__file__)
DIR_PATH = os.path.dirname(FILE_PATH)
REAL_DATA_PATH = os.path.join(os.path.dirname(DIR_PATH), "real_data")

VIDEO_FOLDER_NAME = "20220805_Montserrat_Ivan copia 2"
VIDEO_NAME = "VID_20220805_192531.mp4"
VIDEO_1_PATH = os.path.join(REAL_DATA_PATH, VIDEO_FOLDER_NAME, VIDEO_NAME)

if __name__ == "__main__":

    print(VIDEO_1_PATH)

    assert os.path.isfile(VIDEO_1_PATH)

    print(video_to_hash(path=VIDEO_1_PATH))
