from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from datetime import datetime
from auth.JWT_Handler import SECRET_KEY, ALGORITHM
from auth.JWT_Handler import verify_access_token
from database import get_db
from sqlalchemy.orm import Session
from models.users import User

oauth2_scheme=OAuth2PasswordBearer(tokenUrl="auth/login")
#locall running:-
# def get_current_user(token:str=Depends(oauth2_scheme)):
#     credentials_exception=HTTPException(
#         status_code=status.HTTP_401_UNAUTHORIZED,
#         detail="Could not validate credentials",
#         headers={"WWW-Authenticate": "Bearer"},
#     )
#     try:
#         payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
#         email:str=payload["sub"]
#         if email is None:
#             raise credentials_exception
    
#     except JWTError:
#         raise credentials_exception
    
#     return email

#for production:-
def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
    )
    
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception
        
    email = payload.get("sub")
    if email is None:
        raise credentials_exception
        

    user = db.query(User).filter(User.email == email).first()
    
    if user is None:
        raise credentials_exception
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="User account is deactivated"
        )
        
    return user

