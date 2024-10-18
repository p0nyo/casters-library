from __future__ import annotations

import json
from abc import ABC
from typing import List, Type, Optional, Any

from sqlalchemy import func
from sqlalchemy.orm import scoped_session, Session
from sqlalchemy.orm.exc import NoResultFound
from sqlalchemy import func
import _json

from podcast.domainmodel.model import Podcast, Author
from podcast.adapters.repository import AbstractRepository
# from podcast.adapters.utils import search_string
from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode
# from podcast.browse.services import get_podcasts
import podcast.adapters.repository as repo
from podcast.adapters.orm import authors_table, podcast_categories_table, user_table


# feature 1 test
class SessionContextManager:
    def __init__(self, session_factory):
        self.__session_factory = session_factory
        self.__session = scoped_session(self.__session_factory)

    def __enter__(self):
        return self

    def __exit__(self, *args):
        self.rollback()

    @property
    def session(self):
        return self.__session

    def commit(self):
        self.__session.commit()

    def rollback(self):
        self.__session.rollback()

    def reset_session(self):
        # this method can be used e.g. to allow Flask to start a new session for each http request,
        # via the 'before_request' callback
        self.close_current_session()
        self.__session = scoped_session(self.__session_factory)

    def close_current_session(self):
        if not self.__session is None:
            self.__session.close()


class SqlAlchemyRepository(AbstractRepository, ABC):

    def __init__(self, session_factory):
        self._session_cm = SessionContextManager(session_factory)

    def close_session(self):
        self._session_cm.close_current_session()

    def reset_session(self):
        self._session_cm.reset_session()

    # region Podcast_data
    def get_podcasts(self, sorting: bool = False) -> list[Type[Podcast]]:
        podcasts = self._session_cm.session.query(Podcast).all()
        return podcasts

    def get_podcast(self, podcast_id: int) -> Podcast:
        podcast = None
        try:
            query = self._session_cm.session.query(Podcast).filter(
                Podcast._id == podcast_id)
            podcast = query.one()
        except NoResultFound:
            print(f'Podcast {podcast_id} was not found')

        return podcast

    def get_podcast_id_by_title(self, podcast_title):
        podcast = self._session_cm.session.query(Podcast).filter_by(_title=podcast_title).first()

        # Return the podcast_id if a podcast is found, otherwise return None
        if podcast:
            return podcast._id
        else:
            return None

    def add_review(self, review: Review):
        with self._session_cm as scm:
            # print(f'Adding user: {user}, Type: {type(user)}')
            scm.session.add(review)
            scm.commit()

    def get_reviews_by_podcast_id(self, podcast_id: int) -> list:
        reviews = self._session_cm.session.query(Review).join(Review._reviewed_podcast).filter(
            Podcast._id == podcast_id).all()

        # Return the list of reviews
        return reviews

    def get_user_by_name(self, user_name: str):
        user = self._session_cm.session.query(User).filter_by(_username=user_name).first()

        # Return the podcast_id if a podcast is found, otherwise return None
        if user:
            return user
        else:
            return None

    def get_comment_section(self, podcast_title: str) -> list:
        try:
            query = self._session_cm.session.query(Podcast).filter(Podcast.title == podcast_title)
            podcast = query.one()
            return podcast.deserialize_comments()

        except NoResultFound:
            print(f'Podcast "{podcast_title}" was not found.')
            return []

    def get_review_section(self, podcast_title: str) -> list:
        try:
            query = self._session_cm.session.query(Podcast).filter(Podcast.title == podcast_title)
            podcast = query.one()
            return podcast.deserialize_reviews()

        except NoResultFound:
            print(f'Podcast "{podcast_title}" was not found.')
            return []

    def add_podcast(self, podcast: Podcast):
        with self._session_cm as scm:
            scm.session.merge(podcast)
            scm.commit()

    def add_multiple_podcasts(self, podcasts: List[Podcast]):
        with self._session_cm as scm:
            for podcast in podcasts:
                podcast.set_comments = podcast.serialize_comments()
                podcast.user_reviews = podcast.serialize_user_reviews()
                scm.session.add(podcast)
            scm.commit()

    def get_number_of_podcasts(self) -> int:
        num_podcasts = self._session_cm.session.query(Podcast).count()
        return num_podcasts

    # endregion

    # region Author data
    def get_authors(self) -> list[Type[Author]]:
        authors = self._session_cm.session.query(Author).all()
        return authors

    def get_author(self, author_id: int) -> Author:
        author = None
        try:
            query = self._session_cm.session.query(Author).filter(
                Author._id == author_id)
            author = query.one()
        except NoResultFound:
            print(f'Podcast {author_id} was not found')

        return author

    def add_author(self, author: Author):
        with self._session_cm as scm:
            scm.session.merge(author)
            scm.commit()

    def add_multiple_authors(self, authors: List[Author]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for author in authors:
                    if author.name is None:
                        raise ValueError("Author name cannot be None")
                    scm.session.add(author)
            scm.commit()

    def get_number_of_authors(self) -> int:
        num_authors = self._session_cm.session.query(Author).count()
        return num_authors
    def get_first_author(self):
        article = self._session_cm.session.query(Author).first()
        return article

    # endregion

    # region Category_data
    def get_categories(self) -> list[Type[Category]]:
        categories = self._session_cm.session.query(Category).all()
        return categories

    def get_category(self, category_name):
        category = None
        try:
            query = self._session_cm.session.query(Category).filter(
                Category._name == category_name)
            category = query.one()
        except NoResultFound:
            print(f'Podcast {category_name} was not found')

        return category

    def add_category(self, category: Category):
        with self._session_cm as scm:
            scm.session.merge(category)
            scm.commit()

    def add_multiple_categories(self, categories: List[Category]):
        with self._session_cm as scm:
            with scm.session.no_autoflush:
                for category in categories:
                    scm.session.add(category)
            scm.commit()

    # endregion

    # region Episode_data
    def get_episodes(self, sorting: bool = False) -> list[Type[Episode]]:
        pass

    def get_episode(self, episode_id: int) -> Episode:
        pass

    def add_episode(self, episode: Episode):
        with self._session_cm as scm:
            scm.session.merge(episode)
            scm.commit()

    def add_multiple_episodes(self, episode: List[Episode]):
        with self._session_cm as scm:
            for episode in episode:
                scm.session.merge(episode)
            scm.commit()

    def get_number_of_episodes(self) -> List[Episode]:
        pass

    def get_episodes_for_podcast(self, podcast_id: int) -> List[Episode]:
        episodes = []
        try:
            query = self._session_cm.session.query(Episode).filter(
                Episode.podcast_id == podcast_id)
            episodes = query.all()
        except NoResultFound:
            print(f'Podcast {podcast_id} was not found')
        return episodes

    def get_number_of_episodes_for_podcast(self, podcast_id: int) -> int:
        return len(self.get_episodes_for_podcast(podcast_id))

    def search_podcast_by_title(self, title_string: str) -> list[Type[Podcast]]:
        all_podcasts = []

        query = self._session_cm.session.query(Podcast).filter(
            Podcast._title.ilike(f'%{title_string}%'))

        all_podcasts = query.all()
        if not all_podcasts:
            print(f'No titles contained {title_string}')
        return all_podcasts

    def search_podcast_by_author(self, author_name: str) -> List[Podcast]:
        all_podcasts = []

        query = (
            self._session_cm.session.query(Podcast)
            .join(authors_table, Podcast.author_id == authors_table.c.author_id)
            .filter(authors_table.c.author_name.ilike(f'%{author_name}%'))
        )
        all_podcasts = query.all()
        if not all_podcasts:
            print(f'No titles by {author_name}')
        return all_podcasts

    # Needs fixing
    def search_podcast_by_category(self, category_name: str) -> list[Type[Podcast]]:
        """Retrieve podcasts that belong to a specific category by category name."""
        all_podcasts = []

        category_query = self._session_cm.session.query(Category).filter(
            Category._name.ilike(f'%{category_name}%')).first()

        if category_query is None:
            print(f'No category found with name: {category_name}')
            return all_podcasts

        category_id = category_query.id

        podcast_query = (
            self._session_cm.session.query(Podcast)
            .join(podcast_categories_table, podcast_categories_table.c.podcast_id == Podcast._id)
            .filter(podcast_categories_table.c.category_id == category_id)
        )

        all_podcasts = podcast_query.all()

        if not all_podcasts:
            print(f'No podcasts found for category: {category_name}')

        return all_podcasts

    def get_user(self, user_name: str) -> User:
        """Get user object from database by searching for user_name"""
        user = None
        try:
            query = self._session_cm.session.query(User).filter(
                User._username == user_name)
            user = query.one()
        except NoResultFound:
            print(f'User {user_name} was not found')
        return user

    def add_user(self, user: User):
        with self._session_cm as scm:
            print(f'Adding user: {user}, Type: {type(user)}')
            user.subscription_list = user.serialize_subscription_list()
            scm.session.merge(user)
            scm.commit()

    #Implementation for adding and removing podcasts from favorites.
    def get_podcast_by_title_from_db(self, podcast_title: str) -> Type[Podcast] | None:
        podcasts = self._session_cm.session.query(Podcast).all()
        for podcast in podcasts:
            if podcast is not None:
                if podcast.title is not None and podcast.title == podcast_title:
                    return podcast

        print(f'No podcast found with the title "{podcast_title}"')
        return None

    def get_episode_from_db(self, episode_id) -> Type[Episode] | None:
        try:
            query = self._session_cm.session.query(Episode).filter(Episode.episode_id == episode_id)
            episode = query.one()
            return episode

        except NoResultFound:
            print(f'Episode {episode_id} was not found')
            return None



    def add_episode_to_favorite_podcast(self, user_id: int, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")

        # Fetch the user by ID
        user = self._session_cm.session.query(User).filter_by(_id=user_id).first()
        if user is None:
            raise ValueError(f"User with id {user_id} not found.")

        # Ensure the user has a "Favorite Episodes" podcast at index 0
        if len(user.subscription_list) == 0 or user.subscription_list[0].title != 'Favorite Episodes':
            raise ValueError(f"User {user.username} does not have a 'Favorite Episodes' podcast.")

        # Add the episode to the "Favorite Episodes" podcast
        favorite_podcast = user.subscription_list[0]
        if episode not in favorite_podcast.get_episodes:
            favorite_podcast.add_episode(episode)
            self._session_cm.session.commit()

    def add_podcast_to_user_subscription(self, user_id: int, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")

        # Fetch the user by ID
        user = self._session_cm.session.query(User).filter_by(_id=user_id).first()
        if user is None:
            raise ValueError(f"User with id {user_id} not found.")

        # Deserialize the user's subscription list
        user_deserialized_subscriptions = user.deserialize_subscription_list

        # Check if the podcast is not already in the user's subscription list
        if podcast not in user_deserialized_subscriptions:
            user_deserialized_subscriptions.append(podcast)

            # Serialize the updated subscription list back to a string
            user.subscription_list = user.serialize_subscription_list

            # Update the user in the database
            self._session_cm.session.commit()  # Commit the changes to the database
        else:
            print(f'Podcast "{podcast.title}" is already in the subscription list.')

