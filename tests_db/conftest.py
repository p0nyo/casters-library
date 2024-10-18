import pytest
import sys
import os
from pathlib import Path

# Add the root directory to sys.path
project_root = Path(__file__).resolve().parent.parent  # Adjust the number of parent calls if necessary
sys.path.insert(0, str(project_root))

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, clear_mappers

from podcast.adapters import database_repository, populate_repository
from podcast.adapters.orm import mapper_registry, map_model_to_tables

from utils import get_project_root

TEST_DATA_PATH_DATABASE_FULL = str(get_project_root() / "podcast" / "adapters" / "data")
TEST_DATA_PATH_DATABASE_LIMITED = str(get_project_root() / "tests" / "test_data")
data_path_tests = os.path.abspath('tests')
data_path_podcasts = os.path.abspath('podcast')
TEST_DATABASE_URI_IN_MEMORY = 'sqlite://'
TEST_DATABASE_URI_FILE = 'sqlite:///podcasts-test.db'

os.environ['REPOSITORY'] = 'Database'
os.environ['TESTING'] = 'True'

@pytest.fixture(scope="session")
def database_setup():
    # Initiate .env variables

    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_FILE)

    with engine.connect() as connection:
        mapper_registry.metadata.create_all(connection)
        print(mapper_registry.metadata.tables.keys())

        for table in reversed(mapper_registry.metadata.sorted_tables):  # Use metadata.sorted_tables
            connection.execute(table.delete())

        map_model_to_tables()

    session_factory = sessionmaker(autocommit=False, autoflush=True, bind=engine)

    repo_instance = database_repository.SqlAlchemyRepository(session_factory)

    database_mode = True
    populate_repository.populate_db(data_path_tests, repo_instance, database_mode)

    yield engine, session_factory

    with engine.connect() as connection:
        mapper_registry.metadata.drop_all(connection)

@pytest.fixture
def empty_session():
    clear_mappers()
    engine = create_engine(TEST_DATABASE_URI_IN_MEMORY)

    # Establish a connection from the engine
    with engine.connect() as connection:
        # Conditionally create database tables
        mapper_registry.metadata.create_all(connection)

        # Remove any data from the tables
        for table in reversed(mapper_registry.metadata.sorted_tables):
            connection.execute(table.delete())

        # Map models to tables
        map_model_to_tables()

    # Create the database session factory using sessionmaker
    session_factory = sessionmaker(bind=engine)

    # Yield the session object for the test
    session = session_factory()
    yield session

    # Clean up by dropping all tables
    with engine.connect() as connection:
        mapper_registry.metadata.drop_all(connection)

    # Close the session
    session.close()
