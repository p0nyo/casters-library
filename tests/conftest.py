import os

import pytest

from pathlib import Path
from podcast import create_app
from podcast.adapters import memory_repository
from podcast.adapters.memory_repository import MemoryRepository
from os import environ
from dotenv import load_dotenv

TEST_DATA_PATH = Path(__file__).parent / "test_data"

load_dotenv()

@pytest.fixture
def in_memory_repo():
    os.environ['REPOSITORY'] = 'Memory'
    repo = MemoryRepository()
    memory_repository.populate(repo, TEST_DATA_PATH)
    return repo

@pytest.fixture
def client():
    os.environ['REPOSITORY'] = 'Memory'
    my_app = create_app({
        'TESTING': True,
        'TEST_DATA_PATH': TEST_DATA_PATH,
        'WTF_CSRF_ENABLED': False,
        'SECRET_KEY': environ.get('SECRET_KEY'),
    })
    return my_app.test_client()


class AuthenticationManager:
    def __init__(self, client):
        self.__client = client
        
    def login(self, user_name='thorke1234', password='123456789'):
        return self.__client.post('/authentication/login', data={'user_name':user_name,'password':password})
        
    def logout(self):
        return self.__client.get('/authentication/logout')
    
@pytest.fixture
def auth(client):
    return AuthenticationManager(client)
