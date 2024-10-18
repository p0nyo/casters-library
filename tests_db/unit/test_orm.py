import pytest

import json

import datetime

from sqlalchemy import text

from sqlalchemy.exc import IntegrityError

from podcast.description.services import get_podcast
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Episode, Review, Playlist
from tests_db.conftest import empty_session


def add_user(empty_session, username, password):

    empty_session.execute(
        text('INSERT INTO users (user_name, user_password) VALUES (:user_name, :user_password)'),
                          {'user_name': username, 'user_password': password}
    )
    row = empty_session.execute(
        text('SELECT user_id from users where user_name = :user_name'),
                                {'user_name': username}).fetchone()
    return row[0]

def get_user_by_id(empty_session, user_id):
    return empty_session.query(User).filter(User._id == user_id).one()

def add_podcast(empty_session, podcast_title, author):
    new_podcast = Podcast(
        podcast_id=None,
        title=podcast_title,
        author=author,
        image=None,  # Add default or null values
        description="",
        website="",
        itunes_id=None,
        language="English"
    )

    new_podcast._comment_section = json.dumps([])
    new_podcast._user_reviews = json.dumps([])

    empty_session.add(new_podcast)
    empty_session.commit()

    return new_podcast._id

def get_podcast_by_id(empty_session, podcast_id):
    return empty_session.query(Podcast).filter(Podcast._id == podcast_id).one()

def add_review(empty_session, comment, rating, user, podcast):
    new_review = Review(
        review_id=None,
        review_content=comment,
        user_rating=rating,
        user_review=user,
        reviewed_podcast=podcast
    )

    empty_session.add(new_review)
    empty_session.commit()

    return new_review._review_id

def get_review_by_id(empty_session, review_id):
    return empty_session.query(Review).filter(Review._review_id == review_id).one()

def test_adding_users(empty_session):
    add_user(empty_session, 'Andrew', '123456789')
    add_user(empty_session, 'Gillian', '123456789')

    assert repr(empty_session.query(User).all()) == '[<User 1: Andrew>, <User 2: Gillian>]'

def test_adding_users_with_common_user_name(empty_session):
    add_user(empty_session, "Andrew", "1234")

    with pytest.raises(IntegrityError):
        add_user(empty_session, "Andrew", "112")

def test_get_users(empty_session):
    id_1 = add_user(empty_session, 'Andrew', '123456789')
    id_2 = add_user(empty_session, 'Gillian', '123456789')

    user_1 = get_user_by_id(empty_session, id_1)
    user_2 = get_user_by_id(empty_session, id_2)

    assert id_1 == 1
    assert id_2 == 2

    assert repr(user_1) == "<User 1: Andrew>"
    assert repr(user_2) == "<User 2: Gillian>"

def test_adding_podcasts(empty_session):
    author = Author(2, 'Gillian')
    add_podcast(empty_session, 'Podcast 1', author)

    assert repr(empty_session.query(Podcast).one()) == "<Podcast 1: 'Podcast 1' by Gillian>"

def test_get_podcasts(empty_session):
    author = Author(2, 'Gillian')
    id_1 = add_podcast(empty_session, 'Podcast 1', author)
    id_2 = add_podcast(empty_session, 'Podcast 2', author)

    podcast_1 = get_podcast_by_id(empty_session, id_1)
    podcast_2 = get_podcast_by_id(empty_session, id_2)

    assert repr(podcast_1) == "<Podcast 1: 'Podcast 1' by Gillian>"
    assert id_2 == 2
    assert repr(podcast_2) == "<Podcast 2: 'Podcast 2' by Gillian>"


def test_adding_reviews(empty_session):
    author = Author(2, 'Gillian')
    podcast_id = add_podcast(empty_session, 'Podcast 1', author)
    user_id = add_user(empty_session, "Andrew", "1234")

    podcast = get_podcast_by_id(empty_session, podcast_id)
    user = get_user_by_id(empty_session, user_id)

    add_review(empty_session, "I like this podcast", 3.0, user, podcast)

    review = empty_session.query(Review).one()

    assert repr(podcast) == "<Podcast 1: 'Podcast 1' by Gillian>"
    assert repr(user) == "<User 1: Andrew>"

    assert repr(review) == "<Review 1: Andrew gave a rating of 3 on 'Podcast 1'>"
    assert repr(review.review_content) == "'I like this podcast'"

    # Checking if they link back to the User and Podcast object
    assert repr(review.user_review) == "<User 1: Andrew>"
    assert repr(review.reviewed_podcast) == "<Podcast 1: 'Podcast 1' by Gillian>"

    assert review.user_review._id == 1
    assert review.reviewed_podcast._id == 1

def test_get_reviews(empty_session):
    author = Author(2, 'Gillian')
    podcast_id = add_podcast(empty_session, 'Podcast 1', author)
    user_id = add_user(empty_session, "Andrew", "1234")

    podcast = get_podcast_by_id(empty_session, podcast_id)
    user = get_user_by_id(empty_session, user_id)

    review_id = add_review(empty_session, "I like this podcast", 3.0, user, podcast)

    review = get_review_by_id(empty_session, review_id)

    assert review._review_id == 1