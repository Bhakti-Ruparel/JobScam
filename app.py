from fastapi import FastAPI 
from pydantic import BaseModel
from typing import List

app = FastAPI()
class Item(BaseModel):
    id: int
    name: str
    description: str = None
items = []

@app.post("/items/", response_model=Item)
def create_item(item: Item):
    items.append(item)
    return item