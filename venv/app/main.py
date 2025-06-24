from fastapi.params import Body
from fastapi import FastAPI, HTTPException, status
from fastapi import Response
from pydantic import BaseModel
from typing import Optional
import psycopg2
from psycopg2.extras import RealDictCursor
import time
from . import schemas ,utils # If you're inside a FastAPI package
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base
from fastapi import Depends
from sqlalchemy.orm import Session
from .database import get_db  
from . import models
from .routers import posts,users

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

# while True:

#     try:
#         conn = psycopg2.connect(
#             host='localhost',
#             database='fastapi',
#             user='postgres',
#             password='root',
#             cursor_factory=RealDictCursor
#         )
#         cursor = conn.cursor()
                

#         print('✅ Database connection was successful')
#         break
#     except Exception as error:
#         print('❌ Connecting to database failed')
#         print('Error:', error)
#         time.sleep(2)

# @app.get("/")
# async def root():
#     return {"message": "Hello world"}

app.include_router(posts.router)
app.include_router(users.router)
