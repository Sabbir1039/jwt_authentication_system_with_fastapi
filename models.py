from .database import Base
from sqlalchemy import String, Integer, Column, Date

class User(Base):
    __tablename__ = "users"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False, unique=True, index=True)
    email = Column(String, nullable=False, unique=True)
    password = Column(String, nullable=False)