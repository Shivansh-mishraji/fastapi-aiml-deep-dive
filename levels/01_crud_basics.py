from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , Field

class Post(BaseModel):
    id : int = Field(ge=1)
    tittle : str
    content : str

posts_db = [
    {"id": 1, "tittle": "First Post", "content": "Hello World!"},
    {"id": 2, "tittle": "FastAPI Basics", "content": "FastAPI is extremely fast and easy to use."},
    {"id": 3, "tittle": "Pydantic Validation", "content": "Pydantic helps validate data automatically."},
    {"id": 4, "tittle": "FastAPI Basics", "content": "Another post about FastAPI basics."}
]

app = FastAPI()

@app.get("/")
def home_page():
    return {"message":"Welcome to Home Page"}

@app.get("/post/{id}")
def get_post(id:int):
    post = [p for p in posts_db if p['id']==id]
    if len(post)!=0:
        return post
    raise HTTPException(status_code=404,detail="Post Not Found")

@app.get("/posts")
def all_posts(id:int = None, tittle:str=None,content:str=None):
    filtered_posts = posts_db
    if id is not None:
        filtered_posts=[p for p in filtered_posts if p["id"]==id]
    if tittle:
        filtered_posts = [p for p in filtered_posts if p["tittle"]==tittle]
    if content:
        filtered_posts = [p for p in filtered_posts if p["content"]==content]
    if len(filtered_posts)!=0:
        return filtered_posts
    return {
        "Message": "All Posts found Without any Filter",
        "Posts":posts_db
            }

@app.post("/post")
def create_post(post:Post):
    for p in posts_db:      
        if p["id"] == post.id:
            raise HTTPException(status_code=400,
                                detail="Posts Already Exists")
    posts_db.append(dict(post))
    return {"Message":"Post Created Successfully", "Post":post}

@app.put("/post")
def update_post(post:Post):
    for p in posts_db:
        if p["id"]== post.id:
            p["tittle"]=post.tittle
            p["content"]= post.content
            return {"Message":"Post updated successfully",
                    "Post":post}
    raise HTTPException(status_code=404, detail="Post does not exist")

@app.delete("/post")
def delete_post(id:int):
    for p in posts_db:
        if p['id']==id:
            posts_db.remove(p)
            return {"Message":"Post deleted successfully",
                    "Post":p}
    raise HTTPException(status_code=404, detail="Post not found")
