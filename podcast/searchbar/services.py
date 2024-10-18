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

def search_podcast_by_title(title_string: str, repo: AbstractRepository):
    return repo.search_podcast_by_title(title_string)

def search_podcast_by_author(author_name:str, repo: AbstractRepository):
    return repo.search_podcast_by_author(author_name)

def search_podcast_by_category(category_name:str, repo: AbstractRepository):
    return repo.search_podcast_by_category(category_name)

