from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.contact_model import Contact
from schemas.contact_schema import ContactCreate
import uuid

PAGE_SIZE = 5 

def get_contacts(db: Session, username: str, name=None, contact_no=None, contact_id=None, page=1):
    try:
        query = db.query(Contact).filter(Contact.username == username)  # Restrict to logged-in user

        if name:
            query = query.filter(Contact.name == name)
        if contact_no:
            query = query.filter(Contact.contact_no == contact_no)
        if contact_id:
            query = query.filter(Contact.id == contact_id)

        total_contacts = query.count()
        total_pages = (total_contacts + PAGE_SIZE - 1) // PAGE_SIZE

        if total_contacts == 0:
            raise HTTPException(status_code=404, detail="No contacts found.")

        if page > total_pages:
            raise HTTPException(status_code=400, detail=f"Invalid page number. Only {total_pages} pages available.")

        skip = (page - 1) * PAGE_SIZE
        return query.offset(skip).limit(PAGE_SIZE).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving contacts: {str(e)}")


def create_contact(db: Session, contact: ContactCreate, username: str):
    try:
        contact_id = str(uuid.uuid4().int)[:18]  # Generate a larger numeric ID
        db_contact = Contact(id=contact_id, name=contact.name, contact_no=contact.contact_no, username=username)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating contact: {str(e)}")


def update_contact(db: Session, contact_id: str, username: str, name: str = None, contact_no: int = None):
    try:
        contact = db.query(Contact).filter(Contact.id == contact_id, Contact.username == username).first()
        if not contact:
            raise HTTPException(status_code=404, detail="ID does not exist.")

        if name:
            contact.name = name
        if contact_no is not None:
            contact.contact_no = contact_no
        db.commit()
        db.refresh(contact)
        return contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error updating contact: {str(e)}")


def delete_contact(db: Session, contact_id: str, username: str):
    try:
        contact = db.query(Contact).filter(Contact.id == contact_id, Contact.username == username).first()
        if not contact:
            raise HTTPException(status_code=404, detail="ID does not exist.")

        db.delete(contact)
        db.commit()
        return {"message": "Contact deleted successfully."}
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting contact: {str(e)}")
