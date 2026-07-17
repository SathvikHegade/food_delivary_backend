from datetime import datetime, timedelta, timezone
from jose import jwt,JWTError
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

def create_access_token(data: dict):
    """
    Generates a secure, signed JSON Web Token (JWT) that expires after 30 minutes.
    """
    to_encode = data.copy()
    
    # Calculate the expiration timestamp (Current Time + 30 Minutes)
    expire = datetime.now(timezone.utc) + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    
    # Update the payload with the expiration field ('exp')
    to_encode.update({"exp": expire})
    
    # Sign and encode the token using our secret key and SHA256 algorithm
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    
    return encoded_jwt

def verify_access_token(token: str):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        return None