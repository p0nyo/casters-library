import pytest
from podcast.adapters.memory_repository import MemoryRepository
from podcast.domainmodel.model import Podcast, Author

@pytest.fixture
def my_memory_repo():
    return MemoryRepository()

@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")

@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")

def test_memory_repo_add_podcast(my_memory_repo,my_podcast):
    my_memory_repo.add_podcast(my_podcast)
    assert repr(type(my_memory_repo.get_podcasts())) ==  "<class 'list'>"
    assert repr(my_memory_repo.get_podcasts()[0]) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

def test_memory_repo_get_podcast(my_memory_repo):
    assert repr(type(my_memory_repo.get_podcasts())) ==  "<class 'list'>"

def test_memory_repo_get_number_of_podcasts(my_memory_repo,my_podcast):
    assert repr(type(my_memory_repo.get_number_of_podcasts())) ==  "<class 'int'>"
    assert my_memory_repo.get_number_of_podcasts() ==  0
    my_memory_repo.add_podcast(my_podcast)
    assert my_memory_repo.get_number_of_podcasts() ==  1
