from typing import Optional
from unicodedata import category
from fastapi import Body, FastAPI, Response, status, HTTPException
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

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i


@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.get(r"/posts")
def get_posts():
    return {"data": my_posts}

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(new_post: Post):
    post_dict = new_post.dict()
    post_dict['id']= randrange(0, 1000000)
    my_posts.append(post_dict)
    return {"data": post_dict}

@app.get("/posts/{id}")
def get_post(id: int, response: Response):
    post = find_posts(id)
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with {id} was not found")
    return {"post details": post }

@app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int):
    index = find_index_post(id)
    my_posts.pop(id)
    return Response(status_code=status.HTTP_204_NO_CONTENT)


if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000) 


