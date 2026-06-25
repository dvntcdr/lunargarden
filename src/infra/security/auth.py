from pwdlib import PasswordHash


pwd_hash = PasswordHash.recommended()


def hash_password(password: str) -> str:
    return pwd_hash.hash(password)


def verify_password(password: str, hash: str) -> bool:
    return pwd_hash.verify(password, hash)
