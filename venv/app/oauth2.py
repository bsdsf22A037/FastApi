from jose import JWTError,jwt
import datetime,timedelta


#SECRET_KEY
SECRET_KEY = "84b4f4d3586f43cc87de15c13740d0b89d49b7efccf679a1293ea7cd3ab44582"


#Algorithm 
ALGORITHM = "HS256"
#Expitation time 
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def creaye_access_token(data : dict):
    to_encode = data.copy()
    Expire = datetime.now() + timedelta(minutes = ACCESS_TOKEN_EXPIRE_MINUTES)
    to_encode.update({"exp":Expire})
    encoded_jwt = jwt.encode(to_encode,SECRET_KEY,algorithm=ALGORITHM)
    return encoded_jwt

from jose import JWTError, jwt
from datetime import datetime, timedelta  # ← Fix here

# SECRET KEY
SECRET_KEY = "84b4f4d3586f43cc87de15c13740d0b89d49b7efccf679a1293ea7cd3ab44582"

# Algorithm
ALGORITHM = "HS256"

# Expiration time in minutes
ACCESS_TOKEN_EXPIRE_MINUTES = 30

def create_access_token(data: dict):  # ← Fix typo: creaye → create
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)  # use UTC time
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt
