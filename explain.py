from typing import Union, Annotated

from fastapi import FastAPI, Header
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

app = FastAPI()


@app.get("/")  # /
def read_root():
    print("read_root")
    return {"Hello": "nice to meet you"}

@app.get("/header")
async def read_items(user_agent: Annotated[str | None, Header()] = None):
    return {"User-Agent": user_agent}

@app.get("/items/{item_id}") # /items/5?q=hello
def read_item(item_id: int, q: Union[str, None] = None): # ?q=hello
    print("read_item", item_id, q)
    return {"item_id": item_id, "q": q}


# /convert?mile=100  --> {"km": 160.9344}    mile * 1.609344
@app.get("/convert")
def convert(mile: float):
    km = mile * 1.609344
    return {"km": km}

# /dollar/{value}  --> {"won": 1200}    value * 1200

@app.post("/items")
async def create_item(item: Item):
    print("create_item", item)
    return item

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, q:str|None = None):
    results = {"item_id": item_id, "item": item, "user": user}
    return results