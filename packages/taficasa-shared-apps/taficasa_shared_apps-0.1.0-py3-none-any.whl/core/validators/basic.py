import re
import uuid
from typing import Optional


def is_valid_uuid(uuid_to_test: str, version: int = 4) -> bool:
    """
    Check if uuid_to_test is a valid UUID.

    Parameters
    ----------
    uuid_to_test : str
    version : {1, 2, 3, 4}

    Returns
    -------`
    `True` if uuid_to_test is a valid UUID, otherwise `False`.

    Examples
    --------
    >>> is_valid_uuid('c9bf9e57-1685-4c89-bafb-ff5af830be8a')
    True
    >>> is_valid_uuid('c9bf9e58')
    False
    """
    try:
        uuid_obj = uuid.UUID(uuid_to_test, version=version)
    except ValueError:
        return False

    return str(uuid_obj) == uuid_to_test


def validate_password(password: str) -> bool:
    """
    Checks if password meets the requirements and if so,
    returns a boolean. Does not sanitize password

    Passwords must be at least 12 characters and contain at least 1 from each
    of the following categories
        * Uppercase letters: A-Z.
        * Lowercase letters: a-z.
        * Numbers: 0-9.
        * Symbols: !@?&#$%

    Passwords cannot contain any whitespace characters, note that
    leading and trailing whitespace is automatically trimmed by
    the serializer.

    TODO Add features to prevent easily guessed password i.e.
        You can't use a password that:
            * Is particularly weak. Example: "password123"
            * You've used before on your account
    """

    if password is None:
        return False

    # Check if password meets length requirements
    if len(password) < 12:
        return False

    # check if password contains any form of whitespace
    whitespace_regex = r"\s"
    whitespace_match = re.search(whitespace_regex, password)

    # If whitespace is found return False
    if whitespace_match is not None:
        return False

    # Check if the password meets the character requirements using regex
    password_regex = (
        r"^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[!@?&#$%])[A-Za-z\d!@?&#$%]{12,}$"
    )

    password_match = re.fullmatch(password_regex, password)

    # If password was matched correctly the return bool
    return password_match is not None
