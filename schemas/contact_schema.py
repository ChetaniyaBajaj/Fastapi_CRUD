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