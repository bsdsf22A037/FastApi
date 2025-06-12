from fastapi import FastAPI
from fastapi.params import Body
app = FastAPI()

@app.get("/")

async def root():
    return {"message ": "Hello world"}

@app.get("/posts")

def get_posts():
    return ("data : this is the post data ")

@app.post("/createpost")
def create_posts(payload: dict = Body(...)):
    print(payload)
    return {"message" : "sucess"}