from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

# for validating the data and its type
class Post(BaseModel):
    title : str
    content : str

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
    print(new_post.title)
    return {"message" : "sucess"}