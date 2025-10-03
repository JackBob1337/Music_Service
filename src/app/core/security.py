from passlib.context import CryptContext

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

MAX_BCRYPT_BYTES = 72 

def safe_truncate(password: str, max_bytes: int = 72) -> str:
    encoded = b""
    for char in password:
        char_bytes = char.encode("utf-8")
        if len(encoded) + len(char_bytes) > max_bytes:
            break
        encoded += char_bytes
    return encoded.decode("utf-8")


def hash_password(password: str) -> str:
    safe_password = safe_truncate(password)
    return pwd_context.hash(safe_password)

def verify_password(plain_password: str, hashed_password: str) -> bool:
    safe_password = safe_truncate(plain_password)
    return pwd_context.verify(safe_password, hashed_password)
