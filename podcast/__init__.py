"""Initialize Flask app."""
from pathlib import Path
from flask import Flask
import os

# imports from SQLAlchemy
from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import sessionmaker, clear_mappers
from sqlalchemy.pool import NullPool

from podcast.domainmodel.model import Podcast
from podcast.adapters.memory_repository import MemoryRepository

# local imports
import podcast.adapters.repository as repo
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.adapters.memory_repository import populate
from podcast.adapters.populate_repository import populate_db
from podcast.adapters.orm import mapper_registry, map_model_to_tables

"""To disable the testing configurations comment out the test test_config variable below
 and the program will automatically switch to the main default configurations"""
# test_config = {'TEST_DATA_PATH': Path('tests/test_data')}

def create_app(test_config=None):
    """Construct the core application."""

    # Create the Flask app object.
    app = Flask(__name__)

    app.config['SECRET_KEY'] = 'secret'

    if os.environ.get('REPOSITORY') == 'Database':
        database_uri = 'sqlite:///podcasts.db'
        app.config['SQLALCHEMY_DATABASE_URI'] = database_uri
        app.config['SQLALCHEMY_ECHO'] = True  # echo SQL statements - useful for debugging
        app.config['TEMPLATES_AUTO_RELOAD'] = True  # HTML changes on page refresh
        app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY')

        # Create a database engine and connect it to the specified database
        database_engine = create_engine(database_uri, connect_args={"check_same_thread": False}, poolclass=NullPool,
                                        echo=False)

        # Create the database session factory using sessionmaker (this has to be done once, in a global manner)
        session_factory = sessionmaker(autocommit=False, autoflush=True, bind=database_engine)

        # Create the SQLAlchemy DatabaseRepository instance for an sqlite3-based repository.
        repo.repo_instance = SqlAlchemyRepository(session_factory)
        data_path = os.path.abspath('podcast')

        if len(inspect(database_engine).get_table_names()) == 0:
            print("REPOPULATING DATABASE...")
            # For testing, or first-time use of the web application, reinitialise the database.
            clear_mappers()
            # Conditionally create database tables.
            mapper_registry.metadata.create_all(database_engine)
            # Remove any data from the tables.
            for table in reversed(mapper_registry.metadata.sorted_tables):
                with database_engine.connect() as conn:
                    conn.execute(table.delete())

            # Generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

            populate_db(data_path, repo.repo_instance)
            print("REPOPULATING DATABASE... FINISHED")

        else:
            # Solely generate mappings that map domain model classes to the database tables.
            map_model_to_tables()

    else:
        if test_config is not None:
            # Load test configuration and override settings
            app.config.from_mapping(test_config)
            data_path = test_config['TEST_DATA_PATH']
        else:
            app.config.from_object('config.Config')
            data_path = Path('podcast') / 'adapters' / 'data'

        repo.repo_instance = MemoryRepository()
        populate(repo.repo_instance, data_path)



    with app.app_context():

        from podcast.home import home
        app.register_blueprint(home.home_blueprint)

        from .description import description
        app.register_blueprint(description.description_blueprint)

        from .library import library
        app.register_blueprint(library.library_blueprint)

        from .playlist import playlist
        app.register_blueprint(playlist.playlist_blueprint)

        from .searchbar import searchbar
        app.register_blueprint(searchbar.searchbar_blueprint)

        from .authentication import authentication
        app.register_blueprint(authentication.authentication_blueprint)

        return app
