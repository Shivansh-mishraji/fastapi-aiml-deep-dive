from fastapi import FastAPI , HTTPException
from pydantic import BaseModel , Field

# pydantic model for post - learned that this validates data automatically
# Field(ge=1) means id must be greater than or equal to 1
# mistake i made : i used Field(gt=1) at first which means id > 1, so id=1 was invalid 
class Post(BaseModel):
    id : int = Field(ge=1)
    tittle : str   # yes this is a typo (should be 'title') but keeping it to be honest
    content : str

# using a list as a fake database for now
# in real projects this would be a real database like postgresql
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

# path parameter - the {id} in the url becomes a function parameter
@app.get("/post/{id}")
def get_post(id:int):
    post = [p for p in posts_db if p['id']==id]
    if len(post)!=0:
        return post
    # learned: must RAISE httpexception, not return it
    # if you return it, fastapi sends it as a 200 ok response (wrong)
    raise HTTPException(status_code=404,detail="Post Not Found")

# query parameters - these come after ? in the url like /posts?id=1&tittle=hello
# mistake i made : forgot to set id=None so it became mandatory and broke the route
# mistake i made : was filtering posts_db each time instead of filtered_posts
#   so if you filtered by id AND tittle, the tittle filter would overwrite the id filter
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

# post request - takes a request body (the Post model)
# mistake i made : used post["id"] to access the id - this crashes because
#   Post is a pydantic OBJECT not a dictionary, should use post.id
# mistake i made : did posts_db.append(post) which adds a pydantic object
#   but posts_db has dicts, so all the get routes would crash after that
#   fix is : dict(post) to convert it first
@app.post("/post")
def create_post(post:Post):
    for p in posts_db:      
        if p["id"] == post.id:
            raise HTTPException(status_code=400,
                                detail="Posts Already Exists")
    posts_db.append(dict(post))
    return {"Message":"Post Created Successfully", "Post":post}

# mistake i made : forgot to add return inside the if block
# without the return, it would update the post AND THEN always raise the 404 error
@app.put("/post")
def update_post(post:Post):
    for p in posts_db:
        if p["id"]== post.id:
            p["tittle"]=post.tittle
            p["content"]= post.content
            return {"Message":"Post updated successfully",
                    "Post":post}
    raise HTTPException(status_code=404, detail="Post does not exist")

# mistake i made : used posts_db.pop(p) where p is a dictionary
# list.pop() needs an INDEX number, not the item itself
# list.remove(p) is the right method - removes by value
@app.delete("/post")
def delete_post(id:int):
    for p in posts_db:
        if p['id']==id:
            posts_db.remove(p)
            return {"Message":"Post deleted successfully",
                    "Post":p}
    raise HTTPException(status_code=404, detail="Post not found")
