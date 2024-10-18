from bisect import insort_left
from typing import List, Iterable


from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Podcast, User
from podcast.adapters.datareader.csvdatareader import CSVDataReader


class MemoryRepository(AbstractRepository):

    def __init__(self):
        self.__podcast = list()
        self.__users = list()


    @property
    def users(self):
        return self.__users

    def add_podcast(self, podcast: Podcast):
        if isinstance(podcast, Podcast):
            insort_left(self.__podcast, podcast)

    def get_podcasts(self):
        return self.__podcast

    def get_number_of_podcasts(self):
        return len(self.__podcast)

    def add_user(self, user):
        self.__users.append(user)

    def get_user(self, user):
        for i in range(len(self.__users)):
            if user.lower().strip() == self.__users[i].username:
                return self.__users[i]
        return None


def populate(repo: MemoryRepository, data_pathway):
    reader = CSVDataReader(data_pathway)
    reader.create_podcast()
    reader.load_episodes_into_podcasts()

    for podcast in reader.podcast_list:
        repo.add_podcast(podcast)


def make_podcast_list_into_dict(podcast_list: list) -> dict:
    podcast_dictionary = dict()
    for podcast in podcast_list:
        if not isinstance(podcast, Podcast):
            pass
        else:
            podcast_dictionary[podcast.title] = podcast
    return podcast_dictionary



