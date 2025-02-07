from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import Optional
from services.crud_service import create_contact, get_contacts, update_contact, delete_contact
from schemas.contact_schema import Contact, ContactCreate
from database.database import SessionLocal
from services.auth import verify_token

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/CreateContact", response_model=Contact, dependencies=[Depends(verify_token)])
def create_contact_route(contact: ContactCreate, db: Session = Depends(get_db), user=Depends(verify_token)):
    return create_contact(db=db, contact=contact, username=user)

@router.get("/ViewContacts", response_model=list[Contact], dependencies=[Depends(verify_token)])
def view_contacts(
    name: Optional[str] = Query(None),
    contact_no: Optional[int] = Query(None),
    contact_id: Optional[str] = Query(None),
    page: int = Query(1, ge=1),
    db: Session = Depends(get_db),
    user=Depends(verify_token)
):
    return get_contacts(db, user, name, contact_no, contact_id, page)

@router.put("/UpdateContact", response_model=Contact, dependencies=[Depends(verify_token)])
def update_contact_details(contact_id: str, name: Optional[str] = None, contact_no: Optional[int] = None, db: Session = Depends(get_db), user=Depends(verify_token)):
    return update_contact(db, contact_id, user, name, contact_no)

@router.delete("/DeleteContact", dependencies=[Depends(verify_token)])
def delete_contact_details(contact_id: str, db: Session = Depends(get_db), user=Depends(verify_token)):
    return delete_contact(db, contact_id, user)
