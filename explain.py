from typing import Union

from fastapi import FastAPI
from pydantic import BaseModel


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

app = FastAPI()


@app.get("/")  # /
def read_root():
    print("read_root")
    return {"Hello": "nice to meet you"}


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