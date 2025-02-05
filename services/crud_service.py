from sqlalchemy.orm import Session
from models.contact_model import Contact
from schemas.contact_schema import ContactCreate

# Create a new contact
def create_contact(db: Session, contact: ContactCreate):
    db_contact = Contact(name=contact.name, contact_no=contact.contact_no)  # Don't include id here
    db.add(db_contact)
    db.commit()
    db.refresh(db_contact)
    return db_contact

# Get all contacts
def get_contacts(db: Session, skip: int = 0, limit: int = 100):
    return db.query(Contact).offset(skip).limit(limit).all()

# Get a contact by ID
def get_contact(db: Session, contact_id: int):
    return db.query(Contact).filter(Contact.id == contact_id).first()

# Update a contact by ID
def update_contact(db: Session, contact_id: int, contact: ContactCreate):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db_contact.name = contact.name
        db_contact.contact_no = contact.contact_no
        db.commit()
        db.refresh(db_contact)
    return db_contact

# Delete a contact by ID
def delete_contact(db: Session, contact_id: int):
    db_contact = db.query(Contact).filter(Contact.id == contact_id).first()
    if db_contact:
        db.delete(db_contact)
        db.commit()
    return db_contact
