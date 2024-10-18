import os
from typing import Optional

from flask import Blueprint, render_template, request, redirect, url_for, session

from podcast.domainmodel.model import User
from podcast.adapters.memory_repository import  make_podcast_list_into_dict
import podcast.adapters.repository as repo
from podcast.authentication.services import get_user_obj
from podcast.adapters.database_repository import SqlAlchemyRepository


from podcast.authentication.authentication import login_required

playlist_blueprint = Blueprint('playlist_bp', __name__)

@playlist_blueprint.route('/playlist/<podcast_title>', methods=['GET', 'POST'])
def playlist(podcast_title):

    podcast_list = repo.repo_instance.get_podcasts()


    if os.environ.get('REPOSITORY') == 'Database':
        if request.method == "GET":
            episode_id = request.form.get('episode_id')
            podcast_title_for_epi: str = request.form.get('podcast_title')

        user_name = session.get('user_name')
        if user_name is None:
            return redirect(url_for('authentication_bp.login'))

        user = repo.repo_instance.get_user(user_name)
        user_playlist = user.deserialize_subscription_list

        # Check if the podcast is already in the user's subscription list
        titles = [podcast.title for podcast in user_playlist]
        if podcast_title not in titles:

            # Assuming you have a method to fetch a podcast instance by title
            podcast_instance = repo.repo_instance.get_podcast_by_title_from_db(podcast_title)

            if podcast_instance is not None:
                repo.repo_instance.add_podcast_to_user_subscription(user.id, podcast_instance)

                # Redirect or render a template as needed
        return render_template("playlist/Playlists.html", User_playlist=user_playlist)



    else:
        podcast_dict = make_podcast_list_into_dict(podcast_list)

        if request.method == "POST":
            episode_id = request.form.get('episode_id')
            podcast_title_for_epi = request.form.get('podcast_title')
            episode = podcast_dict[podcast_title_for_epi].get_episode_with_id(episode_id)

            user_name = session.get('user_name')
            if user_name:
                user = get_user_obj(user_name, repo.repo_instance)
                user.subscription_list[0].get_episodes.append(episode)
                return redirect(url_for("playlist_bp.favorite_episodes"))
            else:
                return redirect(url_for('authentication_bp.login'))

        user_name = session.get('user_name')
        if user_name:
            user = get_user_obj(user_name, repo.repo_instance)
            user_playlist = user.subscription_list

            if podcast_title in podcast_dict and podcast_dict[podcast_title] not in user_playlist:
                user.subscription_list.append(podcast_dict[podcast_title])

        else:
            return redirect(url_for('authentication_bp.login'))

        return render_template("playlist/Playlists.html", User_playlist=user_playlist)



@playlist_blueprint.route('/favorite_episodes', methods=['GET', 'POST'])
def favorite_episodes():

    if os.environ.get('REPOSITORY') == 'Database':
        if request.method == "POST":
            episode_id = request.form.get('episode_id')



    else:
        if request.method == "POST" and "Remove_podcast" in request.form:
            remove_episode(int(request.form.get('Remove_podcast')))
            return redirect(url_for("playlist_bp.favorite_episodes"))

        user_name = session.get('user_name')
        if not user_name:
            return redirect(url_for('authentication_bp.login'))

        user = get_user_obj(user_name, repo.repo_instance)
        fav_epi = user.subscription_list[0].get_episodes
        return render_template("favorite_episodes/favorite_episodes.html", fav_epi=fav_epi)


@playlist_blueprint.route('/playlist/', methods=['GET'])
@login_required
def playlist_empty():

    user_name = session.get('user_name')
    if user_name:
        user = get_user_obj(user_name, repo.repo_instance)
        User_playlist = user.subscription_list
    else:
        return redirect(url_for('authentication_bp.login'))

    if len(User_playlist) > 0:
        return redirect(url_for('playlist_bp.playlist', podcast_title="No_Title"))

    else:
        return render_template("playlist/empty_playlist.html")


@playlist_blueprint.route('/remove_playlist/<podcast_title>', methods=['GET'])
def remove_playlist(podcast_title):

    user_name = session.get('user_name')
    if user_name:
        user = get_user_obj(user_name, repo.repo_instance)
        User_playlist = user.subscription_list
    else:
        return redirect(url_for('authentication_bp.login'))


    for index, podcast in enumerate(User_playlist):
        if podcast.title == podcast_title:
            User_playlist.pop(index)
            break

    return redirect(url_for('playlist_bp.playlist', podcast_title="No_Title"))


def remove_episode(episode_index: int):
    user_name = session.get('user_name')
    if user_name:
        user: User = get_user_obj(user_name, repo.repo_instance)
        user.subscription_list[0].get_episodes.pop(episode_index)

    else:
        return redirect(url_for('authentication_bp.login'))