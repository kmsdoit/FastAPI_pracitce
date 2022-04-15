from typing import Optional,List,String
from pydantic import BaseModel

class ItemBase(BaseModel):
    title : str
    description : Optional[str] = None

class ItemCreate(ItemBase):
    pass

class Item(ItemBase):
    id : int
    owner_id : int

    class config:
        orm_mode = True

class UserBase(BaseModel):
    email :str

class UserCreate(UserBase):
    password : str

class User(UserBase):
    id:int
    is_active : bool

    class config:
        orm_mode = True