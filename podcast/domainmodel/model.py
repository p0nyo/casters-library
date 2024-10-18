from __future__ import annotations

import json
import sys
from typing import List, Iterable, Type
from tokenize import Comment


def validate_non_negative_int(value):
    if value is not None and (not isinstance(value, int) or value < 0):
        raise ValueError("ID must be a positive integer or None.")


def validate_non_empty_string(value, field_name="value"):
    if not isinstance(value, str) or not value.strip():
        raise ValueError(f"{field_name} must be a non-empty string.")


class Author:
    def __init__(self, author_id: int, name: str):
        validate_non_negative_int(author_id)
        validate_non_empty_string(name, "Author name")
        self._id = author_id
        self._name = name.strip()
        self.podcast_list = []

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def add_podcast(self, podcast: Podcast):
        if not isinstance(podcast, Podcast):
            raise TypeError("Expected a Podcast instance.")
        if podcast not in self.podcast_list:
            self.podcast_list.append(podcast)

    def remove_podcast(self, podcast: Podcast):
        if podcast in self.podcast_list:
            self.podcast_list.remove(podcast)

    def __repr__(self) -> str:
        return f"<Author {self._id}: {self._name}>"

    def __eq__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.id == other.id

    def __lt__(self, other: object) -> bool:
        if not isinstance(other, Author):
            return False
        return self.name < other.name

    def __hash__(self) -> int:
        return hash(self.id)

class Podcast:
    def __init__(self, podcast_id: int, author: Author, title: str = "Untitled", image: str = None,
                 description: str = "", website: str = "", itunes_id: int = None, language: str = "Unspecified"):
        # validate_non_negative_int(podcast_id)
        self._id = podcast_id
        self._author = author
        validate_non_empty_string(title, "Podcast title")
        self._title = title.strip()
        self._image = image
        self._description = description
        self._language = language
        self._website = website
        self._itunes_id = itunes_id
        self.categories = []
        self.episodes = []
        self._comment_section = []
        self._user_reviews: list[float] = list()
        self._average_review: float = -1.0

    @property
    def id(self) -> int:
        return self._id

    @property
    def get_comments(self) -> list:
        return self._comment_section

    @get_comments.setter
    def set_comments(self, comments: list):
        self._comment_section = comments

    def serialize_comments(self):
        return json.dumps(self._comment_section)

    def deserialize_comments(self):
        if isinstance(self._comment_section, str):
            return json.loads(self._comment_section)

    @property
    def user_reviews(self) -> list:
        return self._user_reviews

    @user_reviews.setter
    def user_reviews(self, reviews: list):
        self._user_reviews = reviews

    def serialize_user_reviews(self):
        return json.dumps(self._user_reviews)

    def deserialize_user_reviews(self):
        if isinstance(self._user_reviews, str):
            return json.loads(self._user_reviews)

    def add_user_review(self, user_review: float):
        self._user_reviews.append(user_review)

    def remove_user_review(self, user_review: float):
        self._user_reviews.remove(user_review)

    def get_average_rating(self) -> float | str:
        this_comment_section = self.serialize_comments()
        if len(this_comment_section) != 0:
            return round(sum(self._user_reviews) / (len(this_comment_section)), 2)
        else:
            return "Podcast has no ratings yet."

    @property
    def average_rating(self) -> float:
        return self._average_review

    def set_average_rating(self, value: float):
        if isinstance(value, float):
            self._average_review = value

    @property
    def get_episodes(self) -> list:
        return self.episodes

    def get_episode_with_id(self, episode_id) -> Episode | int:
        for episode in self.episodes:
            if episode.episode_id == int(episode_id):
                return episode
        raise ValueError("Episode not found.")


    @property
    def get_categories(self) -> list:
        category_name_list = []
        for category in self.categories:
            category_name_list.append(category.name)
        return category_name_list

    @property
    def author(self) -> Author:
        return self._author

    @property
    def itunes_id(self) -> int:
        return self._itunes_id

    @property
    def title(self) -> str:
        return self._title

    @title.setter
    def title(self, new_title: str):
        validate_non_empty_string(new_title, "Podcast title")
        self._title = new_title.strip()

    @property
    def image(self) -> str:
        return self._image

    @image.setter
    def image(self, new_image: str):
        if new_image is not None and not isinstance(new_image, str):
            raise TypeError("Podcast image must be a string or None.")
        self._image = new_image

    @property
    def description(self) -> str:
        return self._description

    @description.setter
    def description(self, new_description: str):
        if not isinstance(new_description, str):
            validate_non_empty_string(new_description, "Podcast description")
        self._description = new_description

    @property
    def language(self) -> str:
        return self._language

    @language.setter
    def language(self, new_language: str):
        if not isinstance(new_language, str):
            raise TypeError("Podcast language must be a string.")
        self._language = new_language

    @property
    def website(self) -> str:
        return self._website

    @website.setter
    def website(self, new_website: str):
        validate_non_empty_string(new_website, "Podcast website")
        self._website = new_website

    def add_category(self, category: Category):
        if not isinstance(category, Category):
            raise TypeError("Expected a Category instance.")
        if category not in self.categories:
            self.categories.append(category)

    def remove_category(self, category: Category):
        if category in self.categories:
            self.categories.remove(category)

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episodes:
            self.episodes.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episodes:
            self.episodes.remove(episode)

    def to_dict(self):
        return {
            'podcast_id': self._id,
            'author': self.author,
            'title': self.title,
            'image': self.image,
            'description': self.description,
            'website': self.website,
            'itunes_id': self.itunes_id,
            'language': self.language,
            'categories': [category.name for category in self.categories],
            'episodes': [episode.to_dict() for episode in self.episodes]
        }

    def __repr__(self):
        return f"<Podcast {self._id}: '{self._title}' by {self._author.name}>"

    def __eq__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Podcast):
            return False
        return self.title < other.title

    def __hash__(self):
        return hash(self.id)

    def __str__(self) -> str:
        return f"<Podcast {self.id}: '{self.title}' by {self.author.name}>\n" \
               f"  Image: {self.image}\n" \
               f"  Description: {self.description}\n" \
               f"  Language: {self.language}\n" \
               f"  Website: {self.website}\n" \
               f"  iTunes ID: {self.itunes_id}\n" \
               f"  Categories: {', '.join(str(cat) for cat in self.categories)}\n" \
               f"  Episodes: {str([(episode.episode_name, episode.episode_id) for episode in self.episodes])} \n" \

class Category:
    def __init__(self, category_id: int, name: str):
        validate_non_negative_int(category_id)
        validate_non_empty_string(name, "Category name")
        self._id = category_id
        self._name = name.strip()

    @property
    def id(self) -> int:
        return self._id

    @property
    def name(self) -> str:
        return self._name

    @name.setter
    def name(self, new_name: str):
        validate_non_empty_string(new_name, "New name")
        self._name = new_name.strip()

    def __repr__(self) -> str:
        return f"<Category {self._id}: {self._name}>"

    def __eq__(self, other):
        if not isinstance(other, Category):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, Category):
            return False
        return self._name < other.name

    def __hash__(self):
        return hash(self._id)

class User:
    def __init__(self, user_id: int, username: str, password: str):
        # validate_non_negative_int(user_id)
        validate_non_empty_string(username, "Username")
        validate_non_empty_string(password, "Password")
        self._id = user_id
        self._username = username.lower().strip()
        self._password = password
        self._subscription_list = [Podcast(99999, self.username, "Favorited Episodes",
                                           "https://previews.123rf.com/images/lkeskinen/lkeskinen1709/lkeskinen170906691/85997053-favorite-word-in-a-black-and-white-design-rubber-stamp-isolated-on-white.jpg",
                                           "This is where all your favorite episodes are stored.")]
        self._reviews: List[Review] = list()

    @property
    def id(self) -> int:
        return self._id

    @property
    def username(self):
        return self._username

    @property
    def password(self):
        return self._password

    @property
    def reviews(self) -> Iterable['Review']:
        return iter(self._reviews)

    def add_review(self, review: Review):
        self._reviews.append(review)

    @property
    def subscription_list(self):
        return self._subscription_list

    @subscription_list.setter
    def subscription_list(self, subscription_list):
        self._subscription_list = subscription_list

    def add_subscription(self, subscription: PodcastSubscription):
        if not isinstance(subscription, PodcastSubscription):
            raise TypeError("Subscription must be a PodcastSubscription object.")
        if subscription not in self._subscription_list:
            self._subscription_list.append(subscription)

    def remove_subscription(self, subscription: PodcastSubscription):
        if subscription in self._subscription_list:
            self._subscription_list.remove(subscription)

    def serialize_subscription_list(self) -> str:
        serialized_list = [podcast.to_dict() for podcast in self._subscription_list]
        return json.dumps(serialized_list)

    def deserialize_subscription_list(self) -> list[Podcast]:
        if not isinstance(self._subscription_list):
            podcast_dicts = json.loads(self._subscription_list)

            deserialized_podcasts = []
            for podcast_dict in podcast_dicts:
                # Remove 'categories' from the dictionary before passing to Podcast constructor
                podcast_dict.pop('categories', None)

                deserialized_podcasts.append(Podcast(
                    podcast_id=podcast_dict['podcast_id'],
                    author=podcast_dict['author'],
                    title=podcast_dict['title'],
                    image=podcast_dict['image'],
                    description=podcast_dict['description'],
                    website=podcast_dict['website'],
                    itunes_id=podcast_dict['itunes_id'],
                    language=podcast_dict['language']
                ))
            return deserialized_podcasts

    def __repr__(self):
        return f"<User {self.id}: {self.username}>"

    def __eq__(self, other):
        if not isinstance(other, User):
            return False
        return self.id == other.id

    def __lt__(self, other):
        if not isinstance(other, User):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash(self.id)

class PodcastSubscription:
    def __init__(self, sub_id: int, owner: User, podcast: Podcast):
        validate_non_negative_int(sub_id)
        if not isinstance(owner, User):
            raise TypeError("Owner must be a User object.")
        if not isinstance(podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._id = sub_id
        self._owner = owner
        self._podcast = podcast

    @property
    def id(self) -> int:
        return self._id

    @property
    def owner(self) -> User:
        return self._owner

    @owner.setter
    def owner(self, new_owner: User):
        if not isinstance(new_owner, User):
            raise TypeError("Owner must be a User object.")
        self._owner = new_owner

    @property
    def podcast(self) -> Podcast:
        return self._podcast

    @podcast.setter
    def podcast(self, new_podcast: Podcast):
        if not isinstance(new_podcast, Podcast):
            raise TypeError("Podcast must be a Podcast object.")
        self._podcast = new_podcast

    def __repr__(self):
        return f"<PodcastSubscription {self.id}: Owned by {self.owner.username}>"

    def __eq__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id == other.id and self.owner == other.owner and self.podcast == other.podcast

    def __lt__(self, other):
        if not isinstance(other, PodcastSubscription):
            return False
        return self.id < other.id

    def __hash__(self):
        return hash((self.id, self.owner, self.podcast))

class Episode:
    def __init__(self, episode_name: str, episode_length: int, episode_description: str,
                 publication_date: str, episode_id: int, link_to_audio: str, podcast_id: int):

        self.podcast_id = podcast_id
        self._episode_name = episode_name
        self._episode_length = episode_length
        self._episode_description = episode_description
        self._publication_date = publication_date
        self._episode_id = episode_id
        self._link_to_audio = link_to_audio

    @property
    def episode_name(self) -> str:
        return (self._episode_name)

    @property
    def epi_length(self) -> int:
        return (self._episode_length)

    @property
    def episode_description(self) -> str:
        return (self._episode_description)

    @property
    def publication_date(self) -> str:
        return (self._publication_date)

    @property
    def episode_id(self) -> int:
        return (self._episode_id)

    @property
    def link_to_audio(self) -> str:
        return (self._link_to_audio)

    @episode_name.setter
    def episode_name(self, new_name: str):
        self._episode_name = new_name

    @episode_description.setter
    def episode_description(self, new_description: str):
        self._episode_description = new_description

    def __repr__(self):
        return f"<Episode {self.episode_name}: {self.episode_description}: {self.publication_date}>"

    def __eq__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.episode_id == other.episode_id

    def __lt__(self, other):
        if not isinstance(other, Episode):
            return False
        return self.episode_id < other.episode_id

    def __hash__(self):
        return hash((self.episode_id, self._episode_name))

    def integer_into_time(self) -> str:
        second = int(self.epi_length)
        hours = second // 3600
        minutes = (second % 3600) // 60
        seconds = second % 60
        return f"{hours:02}:{minutes:02}:{seconds:02}"

class Review:
    def __init__(self, review_id: int, reviewed_podcast: Podcast,
                 user_review: User, user_rating: int, review_content: str):
        # user_review: user that gave the review
        self._review_id = review_id
        self._reviewed_podcast = reviewed_podcast
        self._user_review = user_review
        self._user_rating = user_rating
        self._review_content = review_content

    @property
    def review_id(self) -> int:
        return self._review_id

    @property
    def reviewed_podcast(self) -> str:
        return self._reviewed_podcast

    @property
    def user_review(self) -> User:
        return self._user_review

    @property
    def user_rating(self) -> int:
        return self._user_rating

    @property
    def review_content(self) -> str:
        return self._review_content

    @user_rating.setter
    def user_rating(self, new_rating: int):
        self._user_rating = new_rating

    @review_content.setter
    def review_content(self, new_content: str):
        self._review_content = new_content

    def __repr__(self):
        return f"<Review {self.review_id}: {self.user_review.username} gave a rating of {self.user_rating} on '{self.reviewed_podcast.title}'>"

    def __eq__(self, other):
        if not isinstance(other, Review):
            return False
        else:
            return self.review_id == other.review_id

    def __lt__(self, other):
        if not isinstance(other, Review):
            return False
        else:
            return self.review_id < other.review_id

    def __hash__(self):
        return hash((self.review_id, self.reviewed_podcast))

class Playlist:
    def __init__(self, playlist_id: int, playlist_user: User,
                 playlist_name: str):
        self._playlist_id = playlist_id
        self._playlist_user = playlist_user
        self._playlist_name = playlist_name
        self.episode_list = []

    @property
    def playlist_id(self):
        return self._playlist_id

    @property
    def playlist_user(self):
        return self._playlist_user

    @property
    def playlist_name(self):
        return self._playlist_name

    @playlist_name.setter
    def playlist_name(self, new_name):
        self._playlist_name = new_name

    def add_episode(self, episode: Episode):
        if not isinstance(episode, Episode):
            raise TypeError("Expected an Episode instance.")
        if episode not in self.episode_list:
            self.episode_list.append(episode)

    def remove_episode(self, episode: Episode):
        if episode in self.episode_list:
            self.episode_list.remove(episode)
        else:
            raise IndexError("Episode does not exist")

    def __repr__(self):
        return f"<Playlist {self.playlist_id}: {self.playlist_name} by {self.playlist_user.username}>"

    def __eq__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.playlist_id == other.playlist_id

    def __lt__(self, other):
        if not isinstance(other, Playlist):
            return False
        return self.playlist_id < other.playlist_id

    def __hash__(self):
        return hash((self.playlist_id, self.playlist_name))
