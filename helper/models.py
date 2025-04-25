from sqlalchemy import Column, Integer, String, Boolean
from helper.database import Base

class Token(Base):
    __tablename__ = 'tbl_token'

    id = Column(Integer, primary_key=True, index=True)
    serviceAccount = Column(String, unique=True)
    pladaName = Column(String)
    clientName = Column(String)
    is_active = Column(Boolean, default=True)
    tokenExp = Column(Boolean, default=True)
    tokenVal = Column(String)

class Users(Base):
    __tablename__ = 'Users'

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True)
    username = Column(String, unique=True)
    first_name = Column(String)
    last_name = Column(String)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    role = Column(String)
    phone_number = Column(String)
