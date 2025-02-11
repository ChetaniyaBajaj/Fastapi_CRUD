from fastapi import APIRouter, HTTPException, Query, Depends
from sqlalchemy.orm import Session
from typing import List, Optional
from services.crud_service import create_contact, get_contacts, update_contact, delete_contact
from schemas.contact_schema import Contact, ContactCreate
from database.database import get_db
from services.auth_service import oauth2_scheme, get_current_user

router = APIRouter()

# Create a new contact
@router.post("/CreateContact", response_model=Contact)
def create_contact_route(contact: ContactCreate, db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")
    
    return create_contact(db=db, contact=contact, username=user.username)

# Get all contacts for the authenticated user
@router.get("/ViewContacts", response_model=list[Contact])
def view_contacts(
    name: Optional[str] = Query(None),
    contact_no: Optional[int] = Query(None),
    contact_id: Optional[int] = Query(None),
    page: int = Query(1, ge=1, description="Page number (starts from 1)"),
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    return get_contacts(db, name, contact_no, contact_id, page, user.username)

# Update a contact by ID (only if owned by the user)
@router.put("/UpdateContact", response_model=Contact)
def update_contact_details(
    contact_id: int,
    name: Optional[str] = None,
    contact_no: Optional[int] = None,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    return update_contact(db, contact_id, name, contact_no, user.username)

# Delete a contact by ID (only if owned by the user)
@router.delete("/DeleteContact", response_model=Contact)
def delete_contact_details(
    contact_id: int,
    db: Session = Depends(get_db),
    token: str = Depends(oauth2_scheme)
):
    user = get_current_user(db, token)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid authentication")

    return delete_contact(db, contact_id, user.username)
