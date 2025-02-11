from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database.database import Base

class Contact(Base):
    __tablename__ = "contacts"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True)
    contact_no = Column(Integer, unique=True, index=True)
    username = Column(String, ForeignKey("users.username"), nullable=False)

    owner = relationship("User")
