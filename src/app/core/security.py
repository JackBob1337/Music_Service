import os
import re
import string
from dotenv import load_dotenv
from datetime import datetime, timedelta
from typing import Union, Any
from jose import jwt
from passlib.context import CryptContext

load_dotenv()

MIN_PASSWORD_LEN = 8
SPECIAL_CHARACTERS = string.punctuation

MIN_USERNAME_LEN = 3
MAX_USERNAME_LEN = 15

ACCESS_TOKEN_EXPIRE_MINUTE = 30
REFRESH_TOKEN_EXPIRE_MINUTE = 60 * 24 * 7
ALGORITHM = "HS256"
JWT_SECRET_KEY = os.environ['JWT_SECRET_KEY']
JWT_REFRESH_SECRET_KEY = os.environ['JWT_REFRESH_SECRET_KEY']

pwd_context = CryptContext(schemes=["bcrypt_sha256"], deprecated="auto")

def hash_password(password: str):
    return pwd_context.hash(password)

def verify_password(password: str, hashed_pass: str):
    return pwd_context.verify(password, hashed_pass)

def password_validation(password: str):
    errors = []

    if not password or password.strip() == "":
        errors.append("Password cannot be empty.")
        
    else:
        if len(password) < MIN_PASSWORD_LEN:
            errors.append(f"Password must be at least {MIN_PASSWORD_LEN} characters long.")

        if not any(char.isdigit() for char in password):
            errors.append("Password must contain at least one digit.")

        if not any(char.isupper() for char in password):
            errors.append("Password must contain at least one uppercase letter.")

        if not any(char in SPECIAL_CHARACTERS for char in password):
            errors.append("Password must contain at least one special character.")

    if errors:
        raise ValueError("\n".join(errors))

    return True

def user_name_validator(user_name: str):
    errors =[]

    if not isinstance(user_name, str):
        errors.append("Username must be a string.")
    
    v = user_name.strip()

    if not v or v.strip() == "":
        errors.append("Username cannot be empty.")
        
    if len(v) < MIN_USERNAME_LEN or len(v) > MAX_USERNAME_LEN:
        errors.append(f"Username must be between {MIN_USERNAME_LEN} and {MAX_USERNAME_LEN} characters long.")
    
    if  not re.match("^[A-Za-z0-9_]+$", v):
        errors.append("Username can only contain letters, digits, and underscores.")

    if errors:
        raise ValueError("\n".join(errors))
    return True 
    
def create_access_token(subject: Union[str, Any], expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTE)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encode_jwt = jwt.encode(to_encode, JWT_SECRET_KEY, ALGORITHM)
    return encode_jwt

def create_refresh_token(subject: Union[str, Any], expires_delta: int = None):
    if expires_delta is not None:
        expires_delta = datetime.utcnow() + expires_delta
    else:
        expires_delta = datetime.utcnow() + timedelta(minutes=REFRESH_TOKEN_EXPIRE_MINUTE)

    to_encode = {"exp": expires_delta, "sub": str(subject)}
    encode_jwt = jwt.encode(to_encode, JWT_REFRESH_SECRET_KEY, ALGORITHM)
    return encode_jwt
