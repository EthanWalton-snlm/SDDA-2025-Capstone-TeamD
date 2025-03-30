import hashlib


def encrypt_password(password):
    hash = hashlib.blake2s()

    encoded_string = password.encode()

    hash.update(encoded_string)

    return hash.hexdigest()
