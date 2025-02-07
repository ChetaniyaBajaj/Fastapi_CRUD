from sqlalchemy.orm import Session
from fastapi import HTTPException
from models.contact_model import Contact
from schemas.contact_schema import ContactCreate

PAGE_SIZE = 5 

def get_contacts(db: Session, name=None, contact_no=None, contact_id=None, page=1):
    try:
        query = db.query(Contact)

        # Apply filters if provided
        if name:
            query = query.filter(Contact.name == name)
        if contact_no:
            query = query.filter(Contact.contact_no == contact_no)
        if contact_id:
            query = query.filter(Contact.id == contact_id)

        total_contacts = query.count()
        total_pages = (total_contacts + PAGE_SIZE - 1) // PAGE_SIZE  # Compute total pages

        if total_contacts == 0:
            raise HTTPException(status_code=404, detail="No contacts found.")

        if page > total_pages:
            raise HTTPException(status_code=400, detail=f"Invalid page number. Only {total_pages} pages available.")

        skip = (page - 1) * PAGE_SIZE  # Convert page number to offset
        return query.offset(skip).limit(PAGE_SIZE).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving contact: {str(e)}")


def create_contact(db: Session, contact: ContactCreate):
    try:
        db_contact = Contact(name=contact.name, contact_no=contact.contact_no)
        db.add(db_contact)
        db.commit()
        db.refresh(db_contact)
        return db_contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error creating contact: {str(e)}")


def update_contact(db: Session, contact_id: int, name: str = None, contact_no: int = None):
    try:    
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        
        if contact:
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


def delete_contact(db: Session, contact_id: int):
    try:
        contact = db.query(Contact).filter(Contact.id == contact_id).first()
        if contact:
            db.delete(contact)
            db.commit()
        return contact
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=f"Error deleting contact: {str(e)}")


def get_contacts_count(db: Session, name=None, contact_no=None, contact_id=None):
    try:
        query = db.query(Contact)
        
        if name:
            query = query.filter(Contact.name == name)
        if contact_no:
            query = query.filter(Contact.contact_no == contact_no)
        if contact_id:
            query = query.filter(Contact.id == contact_id)
        
        return query.count() 
    except Exception as e:
        raise HTTPException(status_code=400, detail=f"Error fetching contacts count: {str(e)}")
