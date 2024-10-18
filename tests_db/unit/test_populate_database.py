from sqlalchemy import select, inspect

import pytest

from sqlalchemy.orm import sessionmaker

from podcast.domainmodel.model import Podcast, Author, Review, Episode, Category


def test_database_populate_inspect_table_name(database_setup):
    engine, session_factory = database_setup
    inspector = inspect(engine)
    assert inspector.get_table_names() == [
        'authors',
        'categories',
        'episodes',
        'playlist',
        'podcast_categories',
        'podcasts',
        'reviews',
        'user_to_favorite_podcasts',
        'users'
    ]

def test_database_populate_select_all_podcasts(database_setup):
    engine, session_factory = database_setup
    Session = sessionmaker(bind=engine)
    session = Session()

    podcasts = session.query(Podcast).all()
    podcast_name_list = []

    for podcast in podcasts:
        podcast_name_list.append(podcast.title)

    assert repr(podcasts[0]) == "<Podcast 2: 'Brian Denny Radio' by Brian Denny>"
    assert repr(podcast_name_list[0:5]) == "['Brian Denny Radio', 'Onde Road - Radio Popolare', 'Tallin Messages', 'Bethel Presbyterian Church (EPC) Sermons', 'Mike Safo']"
    session.close()

def test_database_populate_select_all_authors(database_setup):
    engine, session_factory = database_setup
    Session = sessionmaker(bind=engine)
    session = Session()

    authors = session.query(Author).all()
    author_name_list = []

    for author in authors:
        author_name_list.append(author.name)

    assert len(authors) > 0
    assert repr(authors[0]) == "<Author 1: Brian Denny>"
    assert repr(author_name_list[0:5]) == "['Brian Denny', 'Radio Popolare', 'Tallin Country Church', 'Eric Toohey', 'msafoschnik']"

def test_database_populate_select_all_reviews(database_setup):
    engine, session_factory = database_setup
    Session = sessionmaker(bind=engine)
    session = Session()

    reviews = session.query(Review).all()

    assert len(reviews) == 0 # No reviews in the database
    assert reviews == []

def test_database_populate_select_all_episodes(database_setup):
    engine, session_factory = database_setup
    Session = sessionmaker(bind=engine)
    session = Session()

    episodes = session.query(Episode).all()
    episode_name_list = []

    for episode in episodes:
        episode_name_list.append(episode.episode_name)

    assert len(episodes) > 0
    assert str(episodes[0].episode_name) == "The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3"
    assert repr(episode_name_list[0:3]) == "['The Mandarian Orange Show Episode 74- Bad Hammer Time, or: 30 Day MoviePass Challenge Part 3', 'Finding yourself in the character by justifying your actions', 'Episode 182 - Lyrically Weak']"

def test_database_populate_select_all_categories(database_setup):
    engine, session_factory = database_setup
    Session = sessionmaker(bind=engine)
    session = Session()

    categories = session.query(Category).all()
    category_name_list = []

    for category in categories:
        category_name_list.append(category.name)

    assert len(categories) > 0
    assert repr(categories[0]) == "<Category 1: Professional>"
    assert repr(category_name_list[0:4]) == "['Professional', 'News & Politics', 'Sports & Recreation', 'Comedy']"
