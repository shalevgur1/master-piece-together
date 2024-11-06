
from sqlalchemy import Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base


# Create a base class for all models
Base = declarative_base()

# Define User model and users table in database
class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password = Column(String)
