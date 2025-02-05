from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from services.crud_service import create_contact, get_contacts, get_contact, update_contact, delete_contact
from schemas.contact_schema import Contact, ContactCreate
from database.database import SessionLocal

router = APIRouter()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Create a new contact
@router.post("/CreateContact", response_model=Contact)
def create_contact_route(contact: ContactCreate, db: Session = Depends(get_db)):
    return create_contact(db=db, contact=contact)

# Get all contacts
@router.get("/ViewAllContacts", response_model=list[Contact])
def get_contacts_route(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    return get_contacts(db=db, skip=skip, limit=limit)

# Get a contact by ID
@router.get("/GetContactByID", response_model=Contact)
def get_contact_route(contact_id: int, db: Session = Depends(get_db)):
    db_contact = get_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

# Update a contact by ID
@router.put("/UpdateContact", response_model=Contact)
def update_contact_route(contact_id: int, contact: ContactCreate, db: Session = Depends(get_db)):
    db_contact = update_contact(db=db, contact_id=contact_id, contact=contact)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact

# Delete a contact by ID
@router.delete("/DeleteContact", response_model=Contact)
def delete_contact_route(contact_id: int, db: Session = Depends(get_db)):
    db_contact = delete_contact(db=db, contact_id=contact_id)
    if db_contact is None:
        raise HTTPException(status_code=404, detail="Contact not found")
    return db_contact
