from sqlalchemy import (
    Table, Column, Integer, Float, String, DateTime, ForeignKey, Text
)
from sqlalchemy.orm import registry, relationship
from datetime import datetime

from podcast.domainmodel.model import Podcast, Author, Category, User, Review, Episode, Playlist

# Global variable giving access to the MetaData (schema) information of the database
mapper_registry = registry()

authors_table = Table(
    'authors', mapper_registry.metadata,
    Column('author_id', Integer, primary_key=True),
    Column('author_name', String(255), nullable=False)
)

podcast_table = Table(
    'podcasts', mapper_registry.metadata,
    Column('podcast_id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_title', Text, nullable=True),
    Column('podcast_image_url', Text, nullable=True),
    Column('podcast_description', String(255), nullable=True),
    Column('podcast_language', String(255), nullable=True),
    Column('podcast_website_url', String(255), nullable=True),
    Column('author_id', ForeignKey('authors.author_id')),
    Column('podcast_itunes_id', Integer, nullable=True),
    Column('comments', Text, nullable=True),
    Column('reviews', Text, nullable=True),
)

categories_table = Table(
    'categories', mapper_registry.metadata,
    Column('category_id', Integer, primary_key=True, autoincrement=True),
    Column('category_name', String(64))  # , nullable=False)
)

podcast_categories_table = Table(
    'podcast_categories', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('category_id', ForeignKey('categories.category_id')),
)

user_to_favorite_podcasts = Table(
    'user_to_favorite_podcasts', mapper_registry.metadata,
    Column('id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
)

episodes_table = Table(
    'episodes', mapper_registry.metadata,
    Column('episode_id', Integer, primary_key=True, autoincrement=True),
    Column('podcast_id', Integer, ForeignKey('podcasts.podcast_id')),
    Column('playlist_id', Integer, ForeignKey('playlist.playlist_id')),
    Column('episode_name', Text, nullable=True),
    Column('episode_length', Integer, nullable=True),
    Column('episode_description', String(255), nullable=True),
    Column('episode_date', Text, nullable=True),
    Column('episode_link', Text, nullable=True),
)

user_table = Table(
    'users', mapper_registry.metadata,
    Column('user_id', Integer, primary_key=True, autoincrement=True),
    Column('user_name', String(255), unique=True),
    Column('user_password', String(255)),
    Column('subscription_list', Text, nullable=True)
)

reviews_table = Table(
    'reviews', mapper_registry.metadata,
    Column('review_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', ForeignKey('users.user_id')),
    Column('podcast_id', ForeignKey('podcasts.podcast_id')),
    Column('rating', Integer),
    Column('comment', Text)
)

playlist_table = Table(
    'playlist', mapper_registry.metadata,
    Column('playlist_id', Integer, primary_key=True, autoincrement=True),
    Column('user_id', Integer, ForeignKey('users.user_id')),
    Column('playlist_name', Text),
)


def map_model_to_tables():
    mapper_registry.map_imperatively(Author, authors_table, properties={
        '_id': authors_table.c.author_id,
        '_name': authors_table.c.author_name,
    })


    mapper_registry.map_imperatively(User, user_table, properties={
        '_id': user_table.c.user_id,
        '_username': user_table.c.user_name,
        '_password': user_table.c.user_password,
        '_subscription_list': user_table.c.subscription_list
    })

    mapper_registry.map_imperatively(Podcast, podcast_table, properties={
        '_id': podcast_table.c.podcast_id,
        '_title': podcast_table.c.podcast_title,
        '_image': podcast_table.c.podcast_image_url,
        '_description': podcast_table.c.podcast_description,
        '_language': podcast_table.c.podcast_language,
        '_website': podcast_table.c.podcast_website_url,
        '_itunes_id': podcast_table.c.podcast_itunes_id,
        '_author': relationship(Author),
        '_Podcast_episodes': relationship(Episode, back_populates='_Episode_podcast'),
        'categories': relationship(Category, secondary=podcast_categories_table),
        '_comment_section': podcast_table.c.comments,
        '_user_reviews': podcast_table.c.reviews
    })


    mapper_registry.map_imperatively(Category, categories_table, properties={
        '_id': categories_table.c.category_id,
        '_name': categories_table.c.category_name
    })

    mapper_registry.map_imperatively(Episode, episodes_table, properties={
        '_episode_id': episodes_table.c.episode_id,
        '_Episode_podcast': relationship(Podcast, back_populates='_Podcast_episodes'),
        '_episode_name': episodes_table.c.episode_name,
        '_episode_length': episodes_table.c.episode_length,
        '_episode_description': episodes_table.c.episode_description,
        '_publication_date': episodes_table.c.episode_date,
        '_link_to_audio': episodes_table.c.episode_link,
        '_Episode_playlist': relationship(Playlist, back_populates='_Playlist_episodes'),
    })


    mapper_registry.map_imperatively(Review, reviews_table, properties={
        '_review_id': reviews_table.c.review_id,
        '_user_rating': reviews_table.c.rating,
        '_review_content': reviews_table.c.comment,
        '_reviewed_podcast': relationship(Podcast),
        '_user_review': relationship(User)
    })

    mapper_registry.map_imperatively(Playlist, playlist_table, properties={
        '_playlist_id': playlist_table.c.playlist_id,
        '_playlist_name': playlist_table.c.playlist_name,
        '_Playlist_episodes': relationship(Episode, back_populates='_Episode_playlist'),
    })