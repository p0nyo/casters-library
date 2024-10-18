from datetime import date, datetime

import pytest

import podcast.adapters.repository as repo
from podcast.adapters.database_repository import SqlAlchemyRepository
from podcast.domainmodel.model import User, Author, Podcast, Comment, Category, Episode, Review, Playlist


def test_repository_can_add_a_user(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    user1 = User(None, 'dbtestuser', 'dbtestuser')
    user2 = User(None, 'dbtestuser2', 'dbtestuser2')
    repo.repo_instance.add_user(user1)
    repo.repo_instance.add_user(user2)

    user1 = repo.repo_instance.get_user('dbtestuser')
    user2 = repo.repo_instance.get_user('dbtestuser2')

    assert user1 != user2
    assert repr(type(user1)) == "<class 'podcast.domainmodel.model.User'>"


def test_repository_can_retrieve_a_user(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    repo.repo_instance.add_user(User(None, 'dbtestuser3', 'dbtestuser3'))

    user = repo.repo_instance.get_user('dbtestuser3')

    assert user == repo.repo_instance.get_user('dbtestuser3')


def test_repository_does_not_retrieve_a_non_existent_user(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    user = repo.repo_instance.get_user('fakeuser')

    assert user == None


def test_repository_can_retrieve_author_count(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    number_of_authors = repo.repo_instance.get_number_of_authors()

    # Check that the query returned 177 Articles.
    assert number_of_authors == 14


def test_repository_can_add_author(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    number_of_authors = repo.repo_instance.get_number_of_authors()

    new_author_id = number_of_authors + 1

    author = Author(number_of_authors + 1, 'testauthor')
    repo.repo_instance.add_author(author)

    assert repo.repo_instance.get_author(new_author_id) == author


def test_repository_can_retrieve_author(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    author = repo.repo_instance.get_author(4)

    # Check that the Article has the expected title.
    assert author.name == 'Eric Toohey'


def test_repository_does_not_retrieve_a_non_existent_author(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    article = repo.repo_instance.get_author(201)
    assert article == None


def test_repository_can_retrieve_categories(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    categories = repo.repo_instance.get_categories()

    assert len(categories) == 25


def test_repository_can_get_first_article(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    author = repo.repo_instance.get_first_author()

    assert author.name == "Brian Denny"


def test_repository_can_add_a_category(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    repo.repo_instance.add_category(Category(None, 'Thriller'))

    category = repo.repo_instance.get_category('Thriller')

    assert repr(category) == "<Category 26: Thriller>"


def test_repository_can_search_podcasts_by_title(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    podcast_results_1 = repo.repo_instance.search_podcast_by_title('Bridge Chri')
    podcast_results_2 = repo.repo_instance.search_podcast_by_title('b')

    assert repr(podcast_results_1) == "[<Podcast 10: 'Bridge Christian Community' by Bridge Christian Community, Dubuque, Iowa>]"
    assert len(podcast_results_2) == 5


def test_repository_can_search_podcasts_by_author(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    podcast_results = repo.repo_instance.search_podcast_by_author('Greg Burdine')

    assert repr(podcast_results) == "[<Podcast 9: 'Faith Baptist Church' by Greg Burdine>]"


def test_repository_can_search_podcasts_by_category(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    podcast_results = repo.repo_instance.search_podcast_by_category('Religion')

    assert repr(podcast_results) == "[<Podcast 4: 'Tallin Messages' by Tallin Country Church>]"


def test_repository_can_retrieve_podcasts(database_setup):
    engine, session_factory = database_setup
    repo.repo_instance = SqlAlchemyRepository(session_factory)

    podcast = repo.repo_instance.get_podcast(2)

    assert repr(podcast) == "<Podcast 2: 'Brian Denny Radio' by Brian Denny>"



