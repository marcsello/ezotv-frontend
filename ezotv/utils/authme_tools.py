#!/usr/bin/env python3
import random
import hashlib
import string
from typing import Tuple


def RSA512SALTED_hash(password_clear: str) -> Tuple[str, str]:  # returns: password, salt
    password_salt = ''.join(random.choice(string.ascii_lowercase + string.digits) for i in range(16))
    password_hashed = hashlib.sha512(password_clear.encode() + password_salt.encode()).hexdigest()

    return (password_hashed, password_salt)

