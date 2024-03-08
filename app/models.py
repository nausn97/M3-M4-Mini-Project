from sqlalchemy import Column, Integer, String, DateTime

from database import Base

class Users(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    password = Column(String)


