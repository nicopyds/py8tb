from pathlib import Path
from datetime import datetime
import subprocess
import json

import pandas as pd


def get_creation_date(file_path: str) -> datetime:
    """
    Extrae la fecha de creación/captura del archivo.

    Intenta primero con ExifTool, que es mucho más fiable para manejar
    HEIC, MP4/MOV y los diferentes metadatos de iPhone/DJI/AKASO.
    """

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
        check=True,
    )

    metadata = json.loads(result.stdout)[0]

    # Orden de preferencia
    for field in (
        "DateTimeOriginal",
        "CreateDate",
        "MediaCreateDate",
        "TrackCreateDate",
    ):
        value = metadata.get(field)

        if not value:
            continue

        # Ejemplo: "2026:08:01 12:12:12"
        for fmt in (
            "%Y:%m:%d %H:%M:%S",
            "%Y:%m:%d %H:%M:%S%z",
            "%Y-%m-%d %H:%M:%S",
            "%Y-%m-%dT%H:%M:%S",
        ):
            try:
                return datetime.strptime(value, fmt)
            except ValueError:
                print(f"No se ha encontrado fecha de creación en: {file_path}")

        return None


def add_creation_date_to_filename(file_path: str) -> str:
    """
    Devuelve una nueva ruta cuyo nombre empieza por:

        FILE_YYYYMMDDHHMMSS_

    Ejemplo:
        IMG_6183.HEIC
        ->
        FILE_20260801121212_IMG_6183.HEIC
    """

    path = Path(file_path)

    creation_date = get_creation_date(file_path)

    if creation_date is not None:

        timestamp = creation_date.strftime("%Y%m%d%H%M%S")

        new_name = f"FILE_{timestamp}_{path.name}"
        return str(path.with_name(new_name))

    else:
        return path


def rename_file(old_path: str, new_path: str) -> str:
    """
    Renames a file from old_path to new_path.

    Returns the new path if successful.
    Raises an exception if the source doesn't exist or the destination
    already exists.
    """

    old_path = Path(old_path)
    new_path = Path(new_path)

    if not old_path.exists():
        raise FileNotFoundError(f"Source file does not exist: {old_path}")

    if new_path.exists():
        raise FileExistsError(f"Destination file already exists: {new_path}")

    old_path.rename(new_path)

    return str(new_path)


path = "/Users/nicolaepopescul/code/streams/py8tb/data/data.csv"
df = pd.read_csv(path)
print(df.shape)
df = df[-df["FilePath"].str.contains(".DS_Store")]
print(df.shape)
# df = df.head()

df["NewPath"] = df["FilePath"].apply(add_creation_date_to_filename)

df.to_excel("df_full.xlsx")
