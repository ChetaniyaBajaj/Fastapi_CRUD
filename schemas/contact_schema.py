from pydantic import BaseModel

class ContactBase(BaseModel):
    name: str
    contact_no: int

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True

class UserCreate(BaseModel):
    username: str
    password: str

class UserLogin(BaseModel):
    username: str
    password: str