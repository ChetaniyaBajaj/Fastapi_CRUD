from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from services.crud_service import create_contact, get_contacts, update_contact, delete_contact
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
@router.get("/ViewContacts", response_model=list[Contact])
def view_contacts(
    name: Optional[str] = Query(None),
    contact_no: Optional[int] = Query(None),
    contact_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    db: Session = Depends(get_db)
):
    return get_contacts(db, name, contact_no, contact_id, page)

# Update a contact by ID
@router.put("/UpdateContact", response_model=Contact)
def update_contact_details(
    contact_id: int,
    name: Optional[str] = None,
    contact_no: Optional[int] = None,
    db: Session = Depends(get_db)
):
    if not any([name, contact_no is not None]):
        raise HTTPException(status_code=400, detail="Please provide at least one of 'name' or 'contact_no'.")
    
    contact = update_contact(db, contact_id, name=name, contact_no=contact_no)
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found.")
    
    return contact

# Delete a contact by ID
@router.delete("/DeleteContact", response_model=Contact)
def delete_contact_details(
    contact_id: int,
    db: Session = Depends(get_db)
):
    contact = delete_contact(db, contact_id)
    
    if not contact:
        raise HTTPException(status_code=404, detail="Contact not found.")
    
    return {"message": "Contact deleted successfully."}
