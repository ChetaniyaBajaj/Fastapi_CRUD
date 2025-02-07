from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base
import uuid

def generate_uuid():
    return str(uuid.uuid4().int)[:18]  # Generate a large numeric ID

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(String(18), primary_key=True, default=generate_uuid)
    name = Column(String(255), nullable=False)
    contact_no = Column(Integer, nullable=False, unique=True)
    username = Column(String(255), ForeignKey("users.username"), nullable=False)  # Hidden from user

    user = relationship("User", back_populates="contacts")

class User(Base):
    __tablename__ = "users"

    username = Column(String(255), primary_key=True, unique=True, nullable=False)
    password = Column(String(255), nullable=False)

    contacts = relationship("Contact", back_populates="user")