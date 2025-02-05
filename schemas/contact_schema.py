from pydantic import BaseModel, field_validator

class ContactBase(BaseModel):
    name: str
    contact_no: str

    @field_validator('contact_no')
    def validate_contact_no(cls, value):
        if not value.isdigit() or len(value) != 10:
            raise ValueError('Enter a Valid Contact Number')
        return value

class ContactCreate(ContactBase):
    pass

class Contact(ContactBase):
    id: int

    class Config:
        orm_mode = True