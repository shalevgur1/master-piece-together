# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import ProgrammingError
from dotenv import load_dotenv
import os
from models import Base

# Load environment variables from .env file
load_dotenv()
MPT_USERS_MPT_USERS_DB_NAME = "mpt_users"

class DBUsersManager():

    def __init__(self):
        """
            Connect to mpt_users db.
            Initialize session maker with the mpt_users db session maker
        """

        # Check for mps_users db (also creates it if needed)
        if _check_mpt_users():
            mpt_users_db_url = f"postgresql://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/{MPT_USERS_DB_NAME}"

            # Create the SQLAlchemy engine for mps_users db
            mpt_users_engine = create_engine(mpt_users_db_url)

            # Create all tables in the database
            Base.metadata.create_all(bind=mpt_users_engine)

            # Create and return the sessionmaker
            mpt_db_session_maker = sessionmaker(autocommit=False, autoflush=False, bind=mpt_users_engine)
            self.mpt_db_session_maker = mpt_db_session_maker

        self.mpt_db_session_maker = None

    def _check_mpt_users():
        """
            Check for the existance of the mpt_users database.
            If it does not exist it is being created.
            If it does exist it is being connected.
        """

        postgres_db_url = f"postgresql://{os.getenv('POSTGRES_USERNAME')}:{os.getenv('POSTGRES_PASSWORD')}@localhost:5432/postgres"
        postgres_db_engine = create_engine(postgres_db_url)

        with postgres_db_engine.connect() as connection:
        # Check if the database exists
            try:
                connection.execute(f"SELECT 1 FROM pg_database WHERE datname='{MPT_USERS_DB_NAME}'")
                print(f"Database '{MPT_USERS_DB_NAME}' already exists.")
                return True
            except ProgrammingError:
                # If the database does not exist, create it
                try:
                    print(f"Database '{MPT_USERS_DB_NAME}' does not exist. Creating...")
                    connection.execute(f"CREATE DATABASE {MPT_USERS_DB_NAME}")
                    print(f"Database '{MPT_USERS_DB_NAME}' created successfully.")
                    return True
                except:
                    print(f"There was a problem with creating '{MPT_USERS_DB_NAME}' database...")
                    return False

    ########################################################################
    #                            CRUD OPERATIONS                           #
    ########################################################################

    def create_user():
        pass

    def get_user():
        pass

    def update_user():
        pass

    def delete_user():
        pass