import os
from datetime import datetime

from flask import Blueprint, render_template, request, redirect, url_for, session

import podcast.adapters.repository as repo
from podcast.adapters.memory_repository import make_podcast_list_into_dict
from podcast.authentication.authentication import login_required
from podcast.playlist.playlist import get_user_obj
import podcast.description.services as services
from podcast.adapters.database_repository import SqlAlchemyRepository

description_blueprint = Blueprint(
    'description_bp', __name__)


@description_blueprint.route('/podcast_description/<podcast_title>', methods=['GET', 'POST'])
def description(podcast_title):

    if os.environ.get('REPOSITORY') == 'Database':
        podcast_list = services.get_podcasts(repo.repo_instance)
        podcast_dict = services.make_podcast_list_into_dict(podcast_list)

        podcast_id = services.get_podcast_id_by_title(podcast_title, repo.repo_instance)
        selected_podcast = None
        if podcast_title in podcast_dict:
            selected_podcast = podcast_dict[podcast_title]

        if request.method == 'POST':
            if 'user_name' in session:
                user = services.get_user_by_name(str(session['user_name']), repo.repo_instance)

                print(type(user))
                user_comment = request.form.get('comment')
                user_rating = float(request.form.get('user_review'))

                print(user_comment, user_rating)

                parsed_comment = (str(session['user_name']).capitalize() +
                                  f''' commented "{user_comment}" and rated this {user_rating}/5. {str(datetime.now().date())}''')
                if user_comment.strip() == "":
                    parsed_comment = str(session[
                                             'user_name']).capitalize() + f" rated this {user_rating}/5. {str(datetime.now().date())}"

                print(parsed_comment)
                services.add_review(selected_podcast, user, user_rating, parsed_comment, repo.repo_instance)

                return redirect(url_for('description_bp.description', podcast_title=podcast_title))
            else:
                return redirect(url_for('authentication_bp.login'))

        reviews_list = services.get_reviews_by_podcast_id(podcast_id, repo.repo_instance)
        comments_list = []
        average_user_rating = 0
        for review in reviews_list:
            comments_list.append(review._review_content)
            average_user_rating += review._user_rating

        if len(reviews_list) == 0:
            average_user_rating = None
        else:
            average_user_rating = float(average_user_rating / len(reviews_list))

        return render_template(
            'description/description.html',
            podcast=selected_podcast,
            comments=comments_list,
            user_reviews=average_user_rating,
        )

    else:
        podcast_list = repo.repo_instance.get_podcasts()
        podcast_dict = make_podcast_list_into_dict(podcast_list)

        if request.method == 'POST':
            if 'user_name' in session:
                make_comment(podcast_title, podcast_dict)
            else:
                return redirect(url_for('authentication_bp.login'))

        if podcast_title in podcast_dict:
            selected_podcast = podcast_dict[podcast_title]
        else:
            user_name = session.get('user_name')
            if user_name:
                user = get_user_obj(user_name, repo.repo_instance)
                selected_podcast = user.subscription_list[0]
                if podcast_title == "favorite_episodes":
                    return render_template("favorite_episodes/favorite_episodes.html",
                                           fav_epi=selected_podcast.get_episodes)

        comments = selected_podcast.get_comments
        user_reviews = selected_podcast.get_average_rating()

        return render_template(
            'description/description.html',
            podcast=selected_podcast,
            comments=comments,
            user_reviews=user_reviews
        )





#@login_required
def make_comment(podcast_title, podcast_dict):

    if os.environ.get('REPOSITORY') == 'Database':
        pass


    else:
        comment = request.form.get('comment')
        individual_user_review = request.form.get('user_review')

        add_user_reviews(podcast_title, podcast_dict)
        parsed_comment = (str(session['user_name']).capitalize() +
                    f''' commented "{comment}" and rated this {individual_user_review}/5. {str(datetime.now().date())}''')
        if comment.strip() == "":
            parsed_comment = str(session['user_name']).capitalize() + f" rated this {individual_user_review}/5. {str(datetime.now().date())}"
        podcast_dict[podcast_title].get_comments.append(parsed_comment)
        return redirect(url_for('description_bp.description', podcast_title=podcast_title))


#@login_required
def add_user_reviews(podcast_title, podcast_dict):
    user_review = float(request.form.get('user_review'))
    review = podcast_dict[podcast_title].get_average_rating()
    podcast_dict[podcast_title].user_reviews.append(user_review)
    podcast_dict[podcast_title].set_average_rating(review)

    return redirect(url_for('description_bp.description', podcast_title=podcast_title))
