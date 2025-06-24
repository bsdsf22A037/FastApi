from pydantic import BaseModel,EmailStr
from typing import Optional


#only fields we want in reponse

class Post_response(BaseModel):
    
    title: str
    content: str
    published: bool

    model_config = {
        "from_attributes": True
    }

class UserCreate(BaseModel):
    email : EmailStr
    password : str

class UserOut(BaseModel):
    id : int
    email : EmailStr

    model_config = {
        "from_attributes": True
    }
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None