import os

from flask import Blueprint, render_template, request

import podcast.adapters.repository as repo
from podcast.domainmodel.model import Podcast, Author
import podcast.searchbar.services as services

searchbar_blueprint = Blueprint(
    'searchbar_bp', __name__)

a1 = Author(1, "Joe Toste")
p1 = Podcast(100, a1, "Joe Toste Podcast - Sales Training Expert")

@searchbar_blueprint.route('/search', methods=['GET', 'POST'])
def searchbar():
    return render_template('search/searchbarpage.html')

@searchbar_blueprint.route('/searchpage', methods=['GET', 'POST'])
def searchpage():

    if os.environ.get("REPOSITORY") == 'Database':
        if request.method == 'POST':
            query = request.form.get('query', '').lower()
            filter_by = request.form.get('filter_by', 'title')
        else:
            query = request.args.get('query').lower()
            filter_by = request.args.get('filter_by')

        # test = [query, filter_by]

        if filter_by == 'title':
            podcasts = services.search_podcast_by_title(query, repo.repo_instance)
        elif filter_by == 'author':
            podcasts = services.search_podcast_by_author(query, repo.repo_instance)
        elif filter_by == 'category':
            podcasts = services.search_podcast_by_category(query, repo.repo_instance)


        page = request.args.get('page', 1, type=int)
        per_page = 30
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(podcasts) + per_page - 1) // per_page

        podcasts_on_page = podcasts[start:end]

        boolean = False
        if len(podcasts_on_page) == 0:
            boolean = True


        return render_template('search/searchpage.html',
            podcasts=podcasts_on_page,
            total_pages=total_pages,
            page=page,
            query = query,
            filter = filter_by,
            no_results=boolean)

    else:
        if request.method == 'POST':
            query = request.form.get('query', '').lower()
            filter_by = request.form.get('filter_by', 'title')
        else:
            query = request.args.get('query').lower()
            filter_by = request.args.get('filter_by')

        podcasts = repo.repo_instance.get_podcasts()
        filtered_podcasts = []

        if filter_by == 'title':
            for podcast in podcasts:
                if query in podcast.title.lower():
                    filtered_podcasts.append(podcast)
        elif filter_by == 'category':
            for podcast in podcasts:
                category = str(podcast.get_categories).lower()
                if query in category:
                    filtered_podcasts.append(podcast)
        elif filter_by == 'author':
            for podcast in podcasts:
                if query in podcast.author.name.lower():
                    filtered_podcasts.append(podcast)

        podcasts = filtered_podcasts

        page = request.args.get('page', 1, type=int)
        per_page = 30
        start = (page - 1) * per_page
        end = start + per_page
        total_pages = (len(podcasts) + per_page - 1) // per_page

        podcasts_on_page = podcasts[start:end]

        boolean = False
        if len(podcasts_on_page) == 0:
            boolean = True

        return render_template('search/searchpage.html',
                               podcasts=podcasts_on_page,
                               total_pages=total_pages,
                               page=page,
                               query=query,
                               filter=filter_by,
                               no_results=boolean)

