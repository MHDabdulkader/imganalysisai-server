from pwdlib import PasswordHash

pwd_context =  PasswordHash.recommended()

def hash_password(password: str) -> str:
    return pwd_context.hash(password)

def password_verify(hashPassword: str, rawPassword: str) -> bool:
    return pwd_context.verify(hashPassword, rawPassword)