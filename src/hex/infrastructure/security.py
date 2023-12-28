from passlib.context import CryptContext


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(raw_password: str):
    return pwd_context.hash(raw_password)


def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)
