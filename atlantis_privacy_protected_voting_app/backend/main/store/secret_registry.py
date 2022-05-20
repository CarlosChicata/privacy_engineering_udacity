#
# Secrets themselves are sensitive, so we don't store them in our codebase. Instead, we store them as environment
# variables
#

import os
import bcrypt
from base64 import b64encode, b64decode
from typing import Optional

UTF_8 = "utf-8"


def get_secret_str(secret_name: str) -> Optional[str]:
    """
    Gets a secret, if it exists. Otherwise, returns None
    """
    return os.getenv(secret_name)


def overwrite_secret_str(secret_name: str, secret_value: str):
    """
    Will overwrite the secret, even if there already is a secret present for the given secret_name
    """
    os.environ[secret_name] = secret_value


def get_secret_bytes(secret_name: str) -> Optional[bytes]:
    """
    Gets a secret, if it exists. Otherwise, returns None
    """
    secret_str = os.getenv(secret_name)
    if not secret_str:
        return None
    return b64decode(secret_str.encode(UTF_8))


def overwrite_secret_bytes(secret_name: str, secret_value: bytes):
    """
    Will overwrite the secret, even if there already is a secret present for the given secret_name
    """
    os.environ[secret_name] = b64encode(secret_value).decode(UTF_8)


def gen_salt() -> bytes:
    return bcrypt.gensalt()
