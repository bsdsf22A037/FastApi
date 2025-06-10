from fastapi import FastAPI
app = FastAPI()

@app.get("/")

async def root():
    return {"message ": "Hello world"}

@app.get("/posts")

def get_posts():
    return ("data : this is the post data ")