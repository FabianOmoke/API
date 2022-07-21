from typing import Optional
from unicodedata import category
from fastapi import Body, FastAPI
import uvicorn
from pydantic import BaseModel
from random import randrange
# from typing import Union


app = FastAPI()


class Post(BaseModel):
    title: str 
    content: str
    published: bool = True
    rating: Optional[int] = None

my_posts = [{"title": "title of post 1", "content":"content of post 1", "id": 1},
            {"title": "favourite foods", "content":"I like lentils", "id": 2} ]

def find_posts(id):
    for p in my_posts:
        if p['id'] == id:
            return p


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get(r"/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts")
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id']= randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/latest")
def get_latest_post():
    latest_post = my_posts[-1]
    return {"detail": latest_post}
@app.get("/posts/{id}")
def get_post(id: int):
    post = find_posts(id)
    return {"post details": post }



if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) 


