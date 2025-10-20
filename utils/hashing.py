import hashlib


def hash_file(path, block_size=65536):
    """Вычисляет md5-хэш файла по частям (не грузит в память целиком)."""
    md5 = hashlib.md5()
    with open(path, "rb") as f:
        for chunk in iter(lambda: f.read(block_size), b""):
            md5.update(chunk)
    return md5.hexdigest()
