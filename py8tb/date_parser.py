"""
Lo vamos a necesitar más adelante en la tercera fase del proyecto
Cuando vamos a reorganizar todos los ficheros/fotos/videos etc
En función de su fecha de creación
"""


def parse_date(filename, split_by_text):

    splitted_filename = filename.split(split_by_text)[1].split(".")[0]

    if (len(splitted_filename) >= 8) and (split_by_text in ["IMG_", "IMG-"]):
        return splitted_filename[:8]

    elif "Screenshot_" in filename:
        return splitted_filename[:10].replace("-", "")

    else:
        return filename


def extract_creation_date_from_photo_name(row):

    row["CreationDate"]
    row["LastModificationDate"]
    filename = row["FileName"]

    if "IMG_" in filename:
        return parse_date(filename=filename, split_by_text="IMG_")

    elif "IMG-" in filename:
        return parse_date(filename=filename, split_by_text="IMG-")

    elif "Screenshot_" in filename:
        return parse_date(filename=filename, split_by_text="Screenshot_")

    else:
        return filename


def parse_date_with_regex(filename):

    import re

    regex_rule = re.compile(pattern="\d{8}|\d{4}-\d{2}-\d{2}")
    results = regex_rule.findall(filename)

    if len(results) > 0:

        if "-" in results[0]:
            return results[0].replace("-", "")

        else:
            return results[0]

    else:
        return filename
