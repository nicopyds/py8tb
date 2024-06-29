from hashlib import sha256


class PhotoToBytes:

    def __init__(self, path: list) -> None:
        self.path = path

    def open_contents(self, path):

        try:
            with open(path, "rb") as f:
                contents = f.read()
                return contents
        except:
            raise Exception(f"Mira bien porque ha fallado {path}")

    def content_to_bytes(self, path):

        return bytearray(self.open_contents(path=path))

    def create_sha256(self):

        result_list = []

        for path_ in self.path:
            hash_file = sha256(string=self.content_to_bytes(path=path_)).hexdigest()
            t = (path_, hash_file)
            result_list.append(t)

        return result_list


def parallel_ptb(splitted_paths):
    ptb = PhotoToBytes(path=splitted_paths)
    return ptb.create_sha256()
