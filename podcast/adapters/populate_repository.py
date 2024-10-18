import os, csv

import pytest
from pathlib2 import Path

from podcast.adapters.repository import AbstractRepository
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def populate_db(data_path: str, repo: AbstractRepository, testing: bool = False):

    reader = CSVDataReader(data_path)
    reader.create_podcast()
    reader.load_episodes_into_podcasts()

    authors = reader.author_dict.values()
    podcasts = reader.podcast_list
    categories = reader.category_dict.values()
    episodes = reader.episode_list

    if reader.podcast_list is None:
        raise Exception("No podcasts found")

    # Add authors to the repo
    repo.add_multiple_authors(authors)

    # Add categories to the repo
    repo.add_multiple_categories(categories)

    # # Add podcasts to the repo
    repo.add_multiple_podcasts(podcasts)

    # Add episodes to the repo
    repo.add_multiple_episodes(episodes)

