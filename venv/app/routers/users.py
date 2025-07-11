from .. import schemas,models,utils
from fastapi import FastAPI, Depends,HTTPException, status,Response,APIRouter
from ..database import get_db  
from sqlalchemy.orm import Session

router = APIRouter()

#create a user 
@router.post("/users", status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate ,db: Session = Depends(get_db)):
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user

#getting information of specific user
@router.get("/users/{id}", response_model=schemas.UserOut)
def get_user(
        id: int,
        db: Session = Depends(get_db)        # 2️⃣ correct query
):
    user = db.query(models.User).filter(models.User.id == id).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"user with id {id} not found",
        )
    return user