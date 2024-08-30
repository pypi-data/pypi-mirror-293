import hashlib
import os


def _get_file_hash(file_path: str) -> str:
    """
    Hashes a file

    Parameters
    ----------
    file_path: str
        path to file to hash

    Returns
    -------
    file_hash: str
    """
    BUF_SIZE = 65536  # lets read stuff in 64kb chunks!

    sha1 = hashlib.sha1()

    with open(file_path, "rb") as f:
        while True:
            data = f.read(BUF_SIZE)
            if not data:
                break
            sha1.update(data)

    return sha1.hexdigest()


def _get_file_size(file_path: str) -> int:
    """
    Return the size of a file in bytes

    Parameters
    ----------
    file_path: str
        path to file

    Returns
    -------
    file_size: int
    """
    return os.path.getsize(file_path)
