from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Review, User, Podcast


class NameNotUniqueNameException(Exception):
    pass


class UnknownUserException(Exception):
    pass


class AuthenticationException(Exception):
    pass

def get_podcasts(repo: AbstractRepository):
    return repo.get_podcasts()

def make_podcast_list_into_dict(podcast_list: list) -> dict:
    podcast_dictionary = dict()
    for podcast in podcast_list:
        if not isinstance(podcast, Podcast):
            pass
        else:
            podcast_dictionary[podcast.title] = podcast
    return podcast_dictionary

def get_podcast(podcast_title: str, repo: AbstractRepository):
    for podcast in repo.get_podcasts():
        if podcast.title == podcast_title:
            return podcast


def add_review(podcast: Podcast, user: User, rating: float, comment: str, repo: AbstractRepository):
    review = Review(review_id=None, user_review=user, reviewed_podcast=podcast, user_rating=rating,
                    review_content=comment)
    repo.add_review(review)


def get_reviews_by_podcast_id(podcast_id: str, repo: AbstractRepository):
    return repo.get_reviews_by_podcast_id(podcast_id)


def get_podcast_id_by_title(podcast_title: str, repo: AbstractRepository):
    return repo.get_podcast_id_by_title(podcast_title)


def get_user_by_name(user_name: str, repo: AbstractRepository):
    return repo.get_user_by_name(user_name)


def make_podcasts_list_into_dict(repo: AbstractRepository) -> dict[str, Podcast]:
    podcasts_list = repo.get_podcasts()
    podcast_dict = dict()

    for podcast in podcasts_list:
        podcast_dict[podcast.title] = podcast

    return podcast_dict
