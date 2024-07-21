import json
from typing import Union, Annotated, List

from fastapi import FastAPI, Header
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy import create_engine, text
# postgresql://postgres:12345678@localhost:5832/postgres
engine = create_engine("postgresql+psycopg2://postgres:12345678@localhost:5832/postgres")


class Item(BaseModel):
    name: str
    description: str | None = None
    price: float
    tax: float | None = None

class User(BaseModel):
    username: str
    full_name: str | None = None

class Member(BaseModel):
    name: str
    role: str 

app = FastAPI()

origins = ["http://localhost:3000",
           ]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

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
    print("convert", mile)
    km = mile * 1.609344
    return {"km": km}

# /dollar/{value}  --> {"won": 1200}    value * 1200

@app.post("/items")
# class Item = {name: str, description: str, price: float, tax: float}
async def create_item(item: Item):
    print("create_item", item)
    return item

@app.put("/items")
async def update_item(item: Item, user: User, q:str|None = None):
    results = {"item": item, "user": user, "q": q}
    return results

@app.put("/items/{item_id}")
async def update_item(item_id: int, item: Item, user: User, q:str|None = None):
    results = {"item_id": item_id, "item": item, "user": user, "q": q}
    return results


# sample code for explanation
def test():
    fin = open("data.json", "rt", encoding="utf-8")
    data = fin.readline()
    print(data)
    fin.close()

    with open("data.json", "rt", encoding="utf-8") as fin:
        data = fin.readline()
        print(data)


### DB CRUD
# read
@app.get("/members")
def read_members():
    # conn = engine.connect()  # database connection like open
    # result = conn.execute(text("SELECT * FROM member"))

    with engine.connect() as conn:
      result = conn.execute(text("SELECT * FROM member"))

    if (result is None):
        return "No data"
    
    response = result.all()
    print("=== response ===", type(response), type(response[0]))
    # === response === <class 'list'> <class 'sqlalchemy.engine.row.Row'>
    print(response)
    # [(2, 'Kim', 'designer'), (3, 'Choi', 'programmer'), (4, 'Andy', 'coder'), (5, 'William', 'manager'), (1, 'Lee', 'coder'), (16, 'Lee', 'william'), (18, 'Brian', 'designer'), (22, 'Tommy', 'designer'), (23, 'Joy', 'designer'), (24, 'Joy', 'designer')]
    # return response
    tmp = []
    for row in response:  # row = (2, 'Kim', 'designer'), <class 'sqlalchemy.engine.row.Row'>
        tmp.append(list(row)) # <class 'sqlalchemy.engine.row.Row'> --> list

    # conn.close()
    print("=== tmp ===")
    print(tmp)
    # [[2, 'Kim', 'designer'], [3, 'Choi', 'programmer'], [4, 'Andy', 'coder'], [5, 'William', 'manager'], [1, 'Lee', 'coder'], [16, 'Lee', 'william'], [18, 'Brian', 'designer'], [22, 'Tommy', 'designer'], [23, 'Joy', 'designer'], [24, 'Joy', 'designer']] 
    return tmp  # list[list] --> json --> frontend

    # return [list(row) for row in response]

# create
# Member(name="Tommy", role="designer")
@app.post("/member")
def create_member(member: Member): # json --> class Member
    # insert into member ("name", "role") values ('Tommy', 'designer');
    print(member.name, member.role) # class

    tmp = member.dict()  # {"name": "Tommy", "role": "designer"}
    print(tmp)  # tmp['name'], tmp['role'] # dict

    # name = member.name
    # role = member.role

    with engine.connect() as conn:
        # member : NG, tmp: OK, member.name, member.role : NG
        conn.execute(text('INSERT INTO member (name, role) VALUES (:name, :role)'),  member.dict()) # tmp
        conn.commit()
    return member


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)