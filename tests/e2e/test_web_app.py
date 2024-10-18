import pytest
from flask import session
import podcast.adapters.repository as repo
from podcast.domainmodel.model import User
from podcast.authentication.services import add_user

def test_home(client):
    response = client.get("/")
    assert response.status_code == 200
    assert b'Welcome to the ultimate podcast library' in response.data

def test_register(client):
    response = client.get('authentication/register')
    assert response.status_code == 200

    response = client.post(
        '/authentication/register',
        data={'user_name': 'thorke1234', 'password': '123456789'}
    )
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'


def test_login(client, auth):
    add_user('thorke1234', '123456789', repo.repo_instance)
    response = client.get('authentication/login')
    assert response.status_code == 200
    auth.login()

    with client:
        response = client.get('/')
        assert response.status_code == 200 
        assert session['user_name'] == 'thorke1234'


def test_logout(client, auth):
    
    auth.login()
    
    with client:
        auth.logout()
        assert 'user_name' not in session
        
def test_podcast_description(client):
    response = client.get("/podcast_description/Brian%20Denny%20Radio")
    assert response.status_code == 200
    
    assert b'5-in-1: Brian Denny' in response.data
    assert b'Brian Denny Radio' in response.data
    
def test_searchbar(client):
    response = client.post('/searchpage', data={'query': 'radio', 'filter_by': 'title'})
    assert response.status_code == 200
    
    assert b'Onde Road - Radio Popolare' in response.data
    assert b'Brian Denny Radio' in response.data
    
def test_library(client):
    response = client.get('/library')
    assert response.status_code == 200
    
    assert b'Bethel Presbyterian Church (EPC) Sermons' in response.data
    assert b'Library' in response.data
    
def test_playlist_not_logged_in(client):
    response = client.get('/playlist/No_Title')
    assert response.status_code == 302
    assert response.headers['Location'] == '/authentication/login'
        
def test_playlist_logged_in(client, auth):
    add_user('thorke1234', '123456789', repo.repo_instance)
    auth.login()
    
    response = client.get('/playlist/No_Title')
    assert response.status_code == 200
    
    assert b'Favorited Episodes' in response.data
    
def test_user_review(client, auth):
    add_user('thorke1234', '123456789', repo.repo_instance)
    auth.login()
    
    response = client.post('podcast_description/Onde%20Road%20-%20Radio%20Popolare', data={'user_review': '3', 'comment': 'Cool'})
    assert response.status_code == 200
    assert b'Cool' in response.data



    
