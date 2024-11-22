from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError, IntegrityError
from dotenv import load_dotenv
import os
from database.models import Base, User
from typing import Optional
import bcrypt
from sqlalchemy import text

from sqlalchemy_utils import database_exists, create_database

# Load environment variables from .env file
load_dotenv()
MPT_USERS_DB_NAME = "mpt_users"

class DBUsersManager():

    def __init__(self):
        """
            Connect to mpt_users db.
            Initialize session maker with the mpt_users db session maker
        """

        print(f"postgresql://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@host.docker.internal:5432/{MPT_USERS_DB_NAME}")
        self.mpt_users_db_url = f"postgresql://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@host.docker.internal:5432/{MPT_USERS_DB_NAME}"

        # Check for mps_users db (also creates it if needed)
        if self._check_mpt_users():

            # Create the SQLAlchemy engine for mps_users db
            self.mpt_users_engine = create_engine(self.mpt_users_db_url)

            # Create all tables in the database
            Base.metadata.create_all(bind=self.mpt_users_engine)

            # Create and return the sessionmaker
            self.mpt_db_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=self.mpt_users_engine)
            print("Database object initialized successfully!")
        else:
            self.mpt_db_session_maker = None

    def _check_mpt_users(self):
        """
            Check for the existance of the mpt_users database.
            If it does not exist it is being created.
            If it does exist it is being connected.
        """

        postgres_db_url = self.mpt_users_db_url
        postgres_db_engine = create_engine(postgres_db_url)

        try:
            if not database_exists(postgres_db_engine.url):
                print(f"Database '{MPT_USERS_DB_NAME}' does not exist. Creating...")
                create_database(postgres_db_engine.url)
                print(f"Database '{MPT_USERS_DB_NAME}' created successfully.")
                return True
            print(f"Database '{MPT_USERS_DB_NAME}' already exists.")
            return True
        except Exception as e:
            print(f"Unexpected error occurred: {str(e)}")
            return False
    
    def _get_session(self):
        """ Get a new session instance """
        if self.mpt_db_session_maker:
            return self.mpt_db_session_maker()
        return None

    def _hash_password(self, password: str) -> str:
        """
        Hash a plain text password using bcrypt.
        """
        salt = bcrypt.gensalt()
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), salt)
        return hashed_password.decode('utf-8')

    def _verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """
        Verify that a plain password matches the hashed password.
        """
        return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8'))


    ########################################################################
    #                            CRUD OPERATIONS                           #
    ########################################################################

    def create_user(self, username: str, email: str, password: str) -> Optional[User]:
        """ Create new user with encrypted password """

        session = self._get_session()

        new_password = self._hash_password(password)
        new_user = User(username=username, email=email, password=new_password)

        try:
            session.add(new_user)
            session.commit()
            session.refresh(new_user)
            return new_user
        except IntegrityError:
            session.rollback()
            print("User with that email already exists.")
            return None
        finally:
            session.close()

    def get_user(self, username: str) -> Optional[User]:
        """
        Return requested user object by 
        given username if found, None if not
        """
        with self._get_session() as session:
            return session.query(User).filter(User.username == username).first()

    def update_user(self, user_id: int, username: Optional[str] = None, email: Optional[str] = None, password: Optional[str] = None) -> Optional[User]:
        """
        Update an existing user's information.

        :param user_id: The ID of the user to update
        :param username: New username, optional
        :param email: New email, optional
        :param password: New password (will be hashed), optional
        :return: The updated user object or None if user not found
        """

        session = self._get_session()

        user = session.query(User).filter(User.id == user_id).first()
        # Check that user exists
        if not user:
            print(f"User with id {user_id} not found.")
            return None
        
        # Update relevant fields in requested user
        if username:
            user.username = username
        if email:
            user.email = email
        if password:
            user.password = self._hash_password(password)
        
        # Update database
        try:
            session.commit()
            session.refresh(user)
            return user
        except IntegrityError:
            session.rollback()
            print("Error updating user.")
            return None
        finally:
            session.close()

    def delete_user(self, user_id: int) -> bool:
        """
        Delete a user by ID.
        :return: True if deletion successful, False otherwise
        """
        session = self._get_session()
        user = session.query(User).filter(User.id == user_id).first()

        # Check that user exists
        if not user:
            print(f"User with id {user_id} not found.")
            return False
        
        # Delete user
        try:
            session.delete(user)
            session.commit()
            return True
        except IntegrityError:
            session.rollback()
            print("Error deleting user.")
            return False
        finally:
            session.close()