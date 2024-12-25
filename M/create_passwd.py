import hashlib


def hash_password(password):
    sha256 = hashlib.sha256()
    sha256.update(password.encode('utf-8'))
    return sha256.hexdigest()

passwd_list = [
    '123',
    '456',
    '789'
]

hashed_passwd_list = [hash_password(p) for p in passwd_list]
print(hashed_passwd_list)
