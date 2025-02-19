from sqlalchemy import Column, String, Integer
from db import initialize_connection

# Initialize the database connection
engine, session, Base = initialize_connection('JR_TRAINING_DB')

class User(Base):
    __tablename__ = 'users'
    
    USER_NAME = Column(String, primary_key=True)
    PASSWORD = Column(String)
    ROLE_ID = Column(Integer)

class DatasetAccess(Base):
    __tablename__ = 'dataset_access'
    
    ROLE_ID = Column(String, primary_key=True)
    ROLE_NAME = Column(String)
    DATASET_ACCESS = Column(String)


