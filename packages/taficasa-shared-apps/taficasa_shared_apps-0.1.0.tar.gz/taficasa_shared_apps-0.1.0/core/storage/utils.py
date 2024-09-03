import os

from cryptography.fernet import Fernet


def convert_bytes_to_storage_hash(bytes: bytes) -> str:
    hash_key = os.environ["STORAGE_KEY_HASH_SECRET"]
    storage_key = Fernet(hash_key).encrypt(bytes)
    return storage_key
