from pathlib import Path
from datetime import datetime
import subprocess
import json
import re
import multiprocessing as mp

import numpy as np
import pandas as pd


# ============================================================
# DATE FROM DJI FILENAME
# ============================================================


def get_date_from_filename(file_path: str) -> tuple[datetime | None, str | None]:
    """
    Extracts a creation date from known DJI filename formats.

    Supported formats:

    1. DJI_YYYYMMDDHHMMSS_...

       Example:
       DJI_20260727190735_0691_D_A001.MP4

    2. dji_mimo_YYYYMMDD_HHMMSS_YYYYMMDDHHMMSS_...

       Example:
       dji_mimo_20260728_173914_20260728173913_1785276790962_photo.JPG

    3. dji_mimo_0_0_0_UNIX_TIMESTAMP_MS.ext

       Example:
       dji_mimo_0_0_0_1786149665048.MP4

    Returns:
        (datetime, source)

        Example:
        (datetime(2026, 7, 27, 19, 7, 35), "DJI_FILENAME")

    If no date can be extracted:
        (None, None)
    """

    filename = Path(file_path).name

    # --------------------------------------------------------
    # 1. DJI_YYYYMMDDHHMMSS_...
    # --------------------------------------------------------

    match = re.search(
        r"^DJI_(20\d{12})_",
        filename,
        re.IGNORECASE,
    )

    if match:
        try:
            return (
                datetime.strptime(
                    match.group(1),
                    "%Y%m%d%H%M%S",
                ),
                "DJI_FILENAME",
            )
        except ValueError:
            pass

    # --------------------------------------------------------
    # 2. dji_mimo_YYYYMMDD_HHMMSS_YYYYMMDDHHMMSS_...
    #
    # Example:
    #
    # dji_mimo_20260728_173914_20260728173913_1785276790962_photo.JPG
    #
    # Use the complete YYYYMMDDHHMMSS timestamp.
    # --------------------------------------------------------

    match = re.search(
        r"^dji_mimo_(20\d{6})_(\d{6})_(20\d{12})_",
        filename,
        re.IGNORECASE,
    )

    if match:
        try:
            return (
                datetime.strptime(
                    match.group(3),
                    "%Y%m%d%H%M%S",
                ),
                "DJI_MIMO_FILENAME",
            )
        except ValueError:
            pass

    # --------------------------------------------------------
    # 3. dji_mimo_0_0_0_UNIX_TIMESTAMP_MS.ext
    #
    # Example:
    #
    # dji_mimo_0_0_0_1786149665048.MP4
    #
    # IMPORTANT:
    # Do NOT use datetime.fromtimestamp(), because that would
    # use the computer's local timezone.
    # --------------------------------------------------------

    match = re.search(
        r"^dji_mimo_0_0_0_(\d{13})\.",
        filename,
        re.IGNORECASE,
    )

    if match:
        try:
            timestamp_ms = int(match.group(1))

            # Interpret Unix timestamp as UTC.
            dt = datetime.utcfromtimestamp(timestamp_ms / 1000)

            return (
                dt,
                "DJI_UNIX_TIMESTAMP",
            )

        except (ValueError, OSError, OverflowError):
            pass

    return None, None


# ============================================================
# CREATION DATE
# ============================================================


def get_creation_date(file_path: str) -> tuple[datetime | None, str | None]:
    """
    Extracts the creation/capture date using the following
    priority:

        1. EXIF / metadata
        2. DJI filename
        3. DJI Unix timestamp
        4. None

    Returns:

        (datetime, source)

    Examples:

        (
            datetime(2026, 8, 1, 12, 12, 12),
            "EXIF:DateTimeOriginal"
        )

        (
            datetime(2026, 7, 27, 19, 7, 35),
            "DJI_FILENAME"
        )

    Dates are returned as naive datetime objects.

    No timezone conversion is performed.
    """

    # ========================================================
    # 1. EXIF / metadata
    # ========================================================

    try:
        result = subprocess.run(
            [
                "exiftool",
                "-j",
                "-DateTimeOriginal",
                "-CreateDate",
                "-MediaCreateDate",
                "-TrackCreateDate",
                file_path,
            ],
            capture_output=True,
            text=True,
            check=False,
        )

        if result.returncode == 0 and result.stdout.strip():

            try:
                metadata = json.loads(result.stdout)[0]

                # Order of preference
                for field in (
                    "DateTimeOriginal",
                    "CreateDate",
                    "MediaCreateDate",
                    "TrackCreateDate",
                ):
                    value = metadata.get(field)

                    if not value:
                        continue

                    # Possible formats returned by ExifTool
                    formats = (
                        "%Y:%m:%d %H:%M:%S",
                        "%Y:%m:%d %H:%M:%S%z",
                        "%Y-%m-%d %H:%M:%S",
                        "%Y-%m-%dT%H:%M:%S",
                    )

                    for fmt in formats:
                        try:
                            dt = datetime.strptime(value, fmt)

                            # Remove timezone information if present.
                            #
                            # We want to preserve the clock time recorded
                            # by the camera, without converting it.
                            dt = dt.replace(tzinfo=None)

                            return (
                                dt,
                                f"EXIF:{field}",
                            )

                        except ValueError:
                            pass

            except (json.JSONDecodeError, IndexError):
                pass

    except FileNotFoundError:
        raise RuntimeError(
            "ExifTool was not found. "
            "Make sure it is installed and available in PATH."
        )

    # ========================================================
    # 2. DJI filename
    # ========================================================

    date_from_filename, source = get_date_from_filename(file_path)

    if date_from_filename is not None:
        return (
            date_from_filename,
            source,
        )

    # ========================================================
    # 3. Nothing found
    # ========================================================

    print(f"No creation date found: {file_path}")

    return None, None


# ============================================================
# NEW PATH
# ============================================================


def add_creation_date_to_filename(file_path: str) -> str:
    """
    Creates the new path:

        FILE_YYYYMMDDHHMMSS_original_filename.ext

    Example:

        IMG_6183.HEIC

    becomes:

        FILE_20260801121212_IMG_6183.HEIC
    """

    path = Path(file_path)

    creation_date, _ = get_creation_date(file_path)

    if creation_date is None:
        return str(path)

    timestamp = creation_date.strftime("%Y%m%d%H%M%S")

    new_name = f"FILE_{timestamp}_{path.name}"

    return str(path.with_name(new_name))


# ============================================================
# RENAME FILE
# ============================================================


def rename_file(old_path: str, new_path: str) -> str:
    """
    Renames a file from old_path to new_path.

    Raises:
        FileNotFoundError:
            Source file does not exist.

        FileExistsError:
            Destination file already exists.

    Returns:
        New path as string.
    """

    old_path = Path(old_path)
    new_path = Path(new_path)

    if not old_path.exists():
        raise FileNotFoundError(f"Source file does not exist: {old_path}")

    if new_path.exists():
        raise FileExistsError(f"Destination file already exists: {new_path}")

    old_path.rename(new_path)

    return str(new_path)


# ============================================================
# PROCESS DATAFRAME
# ============================================================


def process_file(file_path: str) -> pd.Series:
    """
    Processes one file and returns:

        CreationDate
        CreationDateSource
        NewPath
    """

    creation_date, source = get_creation_date(file_path)

    if creation_date is None:
        new_path = str(Path(file_path))

    else:
        timestamp = creation_date.strftime("%Y%m%d%H%M%S")

        path = Path(file_path)

        new_name = f"FILE_{timestamp}_{path.name}"

        new_path = str(path.with_name(new_name))

    return pd.Series(
        {
            "FilePath": file_path,
            "CreationDate": creation_date,
            "CreationDateSource": source,
            "NewPath": new_path,
        }
    )

def process_files(file_paths: list[str]):
    l = []

    for file_path in file_paths:
        r = process_file(file_path=file_path)
        r = r.to_frame().T
        l.append(r)

    return pd.concat(l, axis = 0)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":

    # --------------------------------------------------------
    # Input CSV
    # --------------------------------------------------------

    path = "/Users/nicolaepopescul/code/streams/py8tb/data/data.csv"

    df = pd.read_csv(path)

    print(f"Original dataframe: {df.shape}")

    # --------------------------------------------------------
    # Remove .DS_Store
    # --------------------------------------------------------

    df = df[~df["FilePath"].str.contains(".DS_Store", regex=False, na=False)]
    # df = df.sample(100)

    print(f"After removing .DS_Store: {df.shape}")

    # --------------------------------------------------------
    # Process files
    # --------------------------------------------------------

    paths = df["FilePath"]

    CORES = mp.cpu_count()

    SPLITTED_PATHS = np.array_split(paths, CORES)

    pool = mp.Pool(processes=CORES)

    result_list = pool.map(func=process_files, iterable=SPLITTED_PATHS)

    pool.close()
    pool.join()

    results = pd.concat(result_list)

    print(df.head())
    print(results.head())

    df = df.merge(
        right = results,
        how = "left",
        on = "FilePath"
    )

    # --------------------------------------------------------
    # Save results
    # --------------------------------------------------------

    output_path = "df_full.xlsx"

    df.to_excel(
        output_path,
        index=False,
    )

    print()
    print(f"Results saved to: {output_path}")
