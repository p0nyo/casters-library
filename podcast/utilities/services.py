from typing import Iterable
import random

from podcast.adapters.repository import AbstractRepository
from podcast.domainmodel.model import Article





# ============================================
# Functions to convert dicts to model entities
# ============================================

# def article_to_dict(article: Article):
#     article_dict = {
#         'date': article.date,
#         'title': article.title,
#         'image_hyperlink': article.image_hyperlink
#     }
#     return article_dict
#
#
# def articles_to_dict(articles: Iterable[Article]):
#     return [article_to_dict(article) for article in articles]