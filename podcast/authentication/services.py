from werkzeug.security import generate_password_hash, check_password_hash
from typing import Iterable
import random

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import User


class NameNotUniqueNameException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass


def add_user(user_name: str, password: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is not None:
        raise NameNotUniqueNameException
    # Encrypt password so that the database doesn't store passwords 'in the clear'.
    password_hash = generate_password_hash(password)
    
    # Create and store the new User, with password encrypted.
    user: User = User(user_id=None, username=user_name, password=password_hash)
    repo.add_user(user)


def get_user(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return user_to_dict(user)

def get_user_obj(user_name: str, repo: AbstractRepository):
    user = repo.get_user(user_name)
    if user is None:
        raise UnknownUserException
    return user

def authenticate_user(user_name: str, password: str, repo: AbstractRepository):
    authenticated = False

    user = repo.get_user(user_name)
    if user is not None:
        authenticated = check_password_hash(user.password, password)
    if not authenticated:
        raise AuthenticationException

# Function to convert user model entity to dict
def user_to_dict(user: User):
    user_dict = {
        'user_name': user.username,
        'password': user.password
    }
    return user_dict
