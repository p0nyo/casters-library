import os

from flask import Blueprint, render_template, request, session, redirect, url_for
from flask_wtf import form

import podcast.adapters.repository as repo
from podcast.authentication.services import get_user_obj
import podcast.library.services as services


library_blueprint = Blueprint('library_bp', __name__)

@library_blueprint.route('/library', methods=['GET'])
def library():

    user_name = session.get('user_name')
    if user_name:
        user = get_user_obj(user_name, repo.repo_instance)
        User_playlist = user._subscription_list
    else:
        User_playlist = list()

    podcasts = services.get_podcasts(repo.repo_instance)
    podcast_length = services.get_number_of_podcasts(repo.repo_instance)

    page = request.args.get('page', 1, type=int)
    per_page = 30
    start = (page - 1) * per_page
    end = start + per_page
    total_pages = (podcast_length + per_page - 1) // per_page

    podcasts_on_page = podcasts[start:end]


    return render_template(
        'library/library.html',
        podcasts_on_page=podcasts_on_page,
        total_pages=total_pages,
        page=page,
        User_playlist=User_playlist,
        )