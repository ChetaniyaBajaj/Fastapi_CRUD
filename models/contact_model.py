from sqlalchemy import Column, Integer, String
from database.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    contact_no = Column(String)
