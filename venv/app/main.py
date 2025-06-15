from fastapi.params import Body
from fastapi import FastAPI, HTTPException, status
from fastapi import Response
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import schemas  # If you're inside a FastAPI package
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db  
from . import models


            # your User model lives in models.py (or whatever file you named)
#creating user table 
DATABASE_URL = "postgresql://postgres:root@localhost:5432/fastapi"

# Create the database engine
engine = create_engine(DATABASE_URL)

# Create all tables (in this case, it will create the 'users' table)
Base.metadata.create_all(bind=engine)

print("Tables created successfully.")

app = FastAPI()

# for validating the data and its type
class Post(BaseModel):
    title: str
    content: str
    published: bool = True
    rating: Optional[int] = None

# database connection

while True:

    try:
        conn = psycopg2.connect(
            host='localhost',
            database='fastapi',
            user='postgres',
            password='root',
            cursor_factory=RealDictCursor
        )
        cursor = conn.cursor()
                

        print('✅ Database connection was successful')
        break
    except Exception as error:
        print('❌ Connecting to database failed')
        print('Error:', error)
        time.sleep(2)

# @app.get("/")
# async def root():
#     return {"message": "Hello world"}



#retreiving all the posts 
@app.get("/posts")
def get_posts():
    cursor.execute("""Select * from posts""")
    posts = cursor.fetchall()
   
    
    return {"data": posts}

#creating a post 
@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post_response)
def create_posts(post: Post):
    cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s)RETURNING*""",(post.title,post.content,post.published))
    new_post = cursor.fetchone()
    conn.commit()
    return new_post
#retrieving specific post 
@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute("""SELECT * from posts WHERE id = %s""",(str(id),))
    test_post = cursor.fetchone()
    if not test_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f'post with {id}not found')

    return test_post

#deleting a post
@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))  # Note the comma!
    deleted_post = cursor.fetchone()
    conn.commit()
    
    if deleted_post is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
    return Response(status_code=status.HTTP_204_NO_CONTENT)
#updating a post 
@app.put("/posts/{id}")
def update_post(id : int , post : Post ):
    cursor.execute("""UPDATE posts set title = %s ,content = %s , published = %s WHERE id = %s RETURNING*""",(post.title,post.content,post.published,str(id)))
    updated_post = cursor.fetchone()
    conn.commit()

    if not updated_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f'post with {id}not found')
    return updated_post

#create a user 
@app.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate ,db: Session = Depends(get_db)):
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user
