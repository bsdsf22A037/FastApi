from pydantic import BaseModel

#only fields we want in reponse

class Post_response(BaseModel):
    
    title: str
    content: str
    published: bool

    model_config = {
        "from_attributes": True
    }
