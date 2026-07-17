from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from passlib.context import CryptContext

from database import SessionLocal
from models.users import User
from schemas.users import UserCreate, UserResponse

from auth.JWT_Handler import create_access_token
from fastapi.security import OAuth2PasswordRequestForm
from logger import logger

router=APIRouter()
hashing_pwd= CryptContext(schemes=["bcrypt"], deprecated="auto")

def get_db():
    db=SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/signup",response_model=UserResponse,status_code=status.HTTP_201_CREATED)
def signup(user_data:UserCreate,db:Session=Depends(get_db)):
    existing_user=db.query(User).filter((User.email == user_data.email) | (User.username == user_data.username)).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Username or Email already registered."
        )
    hashed_pwd=hashing_pwd.hash(user_data.password)
    new_user=User(
        username=user_data.username,
        email=user_data.email,
        password=hashed_pwd # Storing the hash string!
    )

    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    logger.info(f"New user registered: {new_user.email}")
    return new_user

@router.post("/login")
def login(user_credential:OAuth2PasswordRequestForm = Depends(),db:Session=Depends(get_db)):
    Acc_checker=db.query(User).filter(User.email==user_credential.username).first()
    if not Acc_checker:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid Credentials"
        )
    

    try:
        pwd_checker=hashing_pwd.verify(user_credential.password, Acc_checker.password)
    except ValueError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication engine error. Please sign up with a new account."
        )
    

    # if not pwd_checker:
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Check your Password once"
    #     )
    if not pwd_checker:
        logger.warning(f"Failed login attempt for user: {user_credential.username}") # Add this
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Check your Password once"
        )

    token_data={"sub": Acc_checker.email}
    access_token = create_access_token(data=token_data)
    
    logger.info(f"User logged in: {user_credential.username}")

    return{
        "access_token": access_token, 
        "token_type": "bearer"
    }
