from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional


# for validating the data and its type
class Post(BaseModel):
    title : str
    content : str
# setting default val 
    published : bool = True
#fully optional 
    rating : Optional[int] = None


app = FastAPI()

@app.get("/")

async def root():
    return {"message ": "Hello world"}

@app.get("/posts")

def get_posts():
    return ("data : this is the post data ")

# @app.post("/createpost")
# def create_posts(payload: dict = Body(...)):
#     print(payload)
#     return {"message" : "sucess"}


@app.post("/createpost")
def create_posts(new_post  : Post):
    print(new_post)
    #converting to dict
    print(new_post.dict())

    return {"message" : "sucess"}