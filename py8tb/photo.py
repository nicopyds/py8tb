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

    @staticmethod
    def photo_to_hash(path):
        hash = sha256(string=PhotoToBytes.content_to_bytes(path=path)).hexdigest()
        return hash

    def create_sha256_list(self):

        result_list = []

        for path_ in self.path:
            hash = self.photo_to_hash(path=path_)
            t = (path_, hash)
            result_list.append(t)

        return result_list


def parallel_ptb(splitted_paths: list) -> list:
    ptb = PhotoToBytes(path=splitted_paths)
    return ptb.create_sha256_list()
