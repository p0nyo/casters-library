from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast

class NonExistentPodcastException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class InvalidPageException(Exception):
    pass


class InvalidSearchKeyException(Exception):
    pass

def get_podcasts(repo: AbstractRepository):
    return repo.get_podcasts()

def get_number_of_podcasts(repo: AbstractRepository):
    return repo.get_number_of_podcasts()


