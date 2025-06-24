from .. import schemas,models
from fastapi import APIRouter, Depends, HTTPException, Response, status
from ..database import get_db  
from sqlalchemy.orm import Session
from typing import Optional,List

router = APIRouter()
#retreiving all the posts 
# @router.get("/posts")
# def get_posts():
#     cursor.execute("""Select * from posts""")
#     posts = cursor.fetchall()
   
    
#     return {"data": posts}

# #creating a post 
# @router.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post_response)
# def create_posts(post: Post):
#     cursor.execute("""INSERT INTO posts (title,content,published) VALUES(%s,%s,%s)RETURNING*""",(post.title,post.content,post.published))
#     new_post = cursor.fetchone()
#     conn.commit()
#     return new_post
# #retrieving specific post 
# @router.get("/posts/{id}")
# def get_post(id:int):
#     cursor.execute("""SELECT * from posts WHERE id = %s""",(str(id),))
#     test_post = cursor.fetchone()
#     if not test_post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f'post with {id}not found')

#     return test_post

# #deleting a post
# @router.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
#     cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING *""", (str(id),))  # Note the comma!
#     deleted_post = cursor.fetchone()
#     conn.commit()
    
#     if deleted_post is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {id} not found")
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)
# #updating a post 
# @router.put("/posts/{id}")
# def update_post(id : int , post : Post ):
#     cursor.execute("""UPDATE posts set title = %s ,content = %s , published = %s WHERE id = %s RETURNING*""",(post.title,post.content,post.published,str(id)))
#     updated_post = cursor.fetchone()
#     conn.commit()

#     if not updated_post:
#         raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail = f'post with {id}not found')
#     return updated_post


#reading all posts
@router.get("/", response_model=List[schemas.Post])
def get_posts(db: Session = Depends(get_db)):
    return db.query(models.Post).all()

#crreating a single posts 
@router.post(
    "/",
    status_code=status.HTTP_201_CREATED,
    response_model=schemas.Post,
)
def create_post(
    post: schemas.Post,    # ← Pydantic schema with title/content/published
    db: Session = Depends(get_db)
):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)         # loads the generated id & defaults
    return new_post

#reading single posts

@router.get("/{id}", response_model=schemas.Post)
def get_post(id: int, db: Session = Depends(get_db)):
    post = db.query(models.Post).filter(models.Post.id == id).first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found",
        )
    return post
#update a post 
@router.put("/{id}", response_model=schemas.Post)
def update_post(
    id: int,
    payload: schemas.Post,     # reuse same schema for PUT
    db: Session = Depends(get_db),
):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found",
        )

    post_query.update(payload.dict(), synchronize_session=False)
    db.commit()
    db.refresh(post)
    return post


#delete a post 

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} not found",
        )
