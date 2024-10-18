import pytest

from pathlib import Path
from podcast.domainmodel.model import Author, Podcast, Category, User, PodcastSubscription, Review, Episode, Playlist
from podcast.adapters.datareader.csvdatareader import CSVDataReader


def test_author_initialization():
    author1 = Author(1, "Brian Denny")
    assert repr(author1) == "<Author 1: Brian Denny>"
    assert author1.name == "Brian Denny"

    with pytest.raises(ValueError):
        author2 = Author(2, "")

    with pytest.raises(ValueError):
        author3 = Author(3, 123)

    author4 = Author(4, " USA Radio   ")
    assert author4.name == "USA Radio"

    author4.name = "Jackson Mumey"
    assert repr(author4) == "<Author 4: Jackson Mumey>"


def test_author_eq():
    author1 = Author(1, "Author A")
    author2 = Author(1, "Author A")
    author3 = Author(3, "Author B")
    assert author1 == author2
    assert author1 != author3
    assert author3 != author2
    assert author3 == author3


def test_author_lt():
    author1 = Author(1, "Jackson Mumey")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    assert author1 < author2
    assert author2 > author3
    assert author1 < author3
    author_list = [author3, author2, author1]
    assert sorted(author_list) == [author1, author3, author2]


def test_author_hash():
    authors = set()
    author1 = Author(1, "Doctor Squee")
    author2 = Author(2, "USA Radio")
    author3 = Author(3, "Jesmond Parish Church")
    authors.add(author1)
    authors.add(author2)
    authors.add(author3)
    assert len(authors) == 3
    assert repr(
        sorted(authors)) == "[<Author 1: Doctor Squee>, <Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"
    authors.discard(author1)
    assert repr(sorted(authors)) == "[<Author 3: Jesmond Parish Church>, <Author 2: USA Radio>]"


def test_author_name_setter():
    author = Author(1, "Doctor Squee")
    author.name = "   USA Radio  "
    assert repr(author) == "<Author 1: USA Radio>"

    with pytest.raises(ValueError):
        author.name = ""

    with pytest.raises(ValueError):
        author.name = 123


def test_category_initialization():
    category1 = Category(1, "Comedy")
    assert repr(category1) == "<Category 1: Comedy>"
    category2 = Category(2, " Christianity ")
    assert repr(category2) == "<Category 2: Christianity>"

    with pytest.raises(ValueError):
        category3 = Category(3, 300)

    category5 = Category(5, " Religion & Spirituality  ")
    assert category5.name == "Religion & Spirituality"

    with pytest.raises(ValueError):
        category1 = Category(4, "")


def test_category_name_setter():
    category1 = Category(6, "Category A")
    assert category1.name == "Category A"

    with pytest.raises(ValueError):
        category1 = Category(7, "")

    with pytest.raises(ValueError):
        category1 = Category(8, 123)


def test_category_eq():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 == category1
    assert category1 != category2
    assert category2 != category3
    assert category1 != "9: Adventure"
    assert category2 != 105


def test_category_hash():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    category_set = set()
    category_set.add(category1)
    category_set.add(category2)
    category_set.add(category3)
    assert sorted(category_set) == [category1, category2, category3]
    category_set.discard(category2)
    category_set.discard(category1)
    assert sorted(category_set) == [category3]


def test_category_lt():
    category1 = Category(9, "Action")
    category2 = Category(10, "Indie")
    category3 = Category(11, "Sports")
    assert category1 < category2
    assert category2 < category3
    assert category3 > category1
    category_list = [category3, category2, category1]
    assert sorted(category_list) == [category1, category2, category3]


# Fixtures to reuse in multiple tests
@pytest.fixture
def my_author():
    return Author(1, "Joe Toste")


@pytest.fixture
def my_podcast(my_author):
    return Podcast(100, my_author, "Joe Toste Podcast - Sales Training Expert")


@pytest.fixture
def my_user():
    return User(1, "Shyamli", "pw12345")


@pytest.fixture
def my_subscription(my_user, my_podcast):
    return PodcastSubscription(1, my_user, my_podcast)


def test_podcast_initialization():
    author1 = Author(1, "Doctor Squee")
    podcast1 = Podcast(2, author1, "My First Podcast")
    assert podcast1.id == 2
    assert podcast1.author == author1
    assert podcast1.title == "My First Podcast"
    assert podcast1.description == ""
    assert podcast1.website == ""

    assert repr(podcast1) == "<Podcast 2: 'My First Podcast' by Doctor Squee>"

    podcast4 = Podcast(123, " ")
    assert podcast4.title is 'Untitled'
    assert podcast4.image is None


def test_podcast_change_title(my_podcast):
    my_podcast.title = "TourMix Podcast"
    assert my_podcast.title == "TourMix Podcast"

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_add_category(my_podcast):
    category = Category(12, "TV & Film")
    my_podcast.add_category(category)
    assert category in my_podcast.categories
    assert len(my_podcast.categories) == 1

    my_podcast.add_category(category)
    my_podcast.add_category(category)
    assert len(my_podcast.categories) == 1


def test_podcast_remove_category(my_podcast):
    category1 = Category(13, "Technology")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category1)
    assert len(my_podcast.categories) == 0

    category2 = Category(14, "Science")
    my_podcast.add_category(category1)
    my_podcast.remove_category(category2)
    assert len(my_podcast.categories) == 1


def test_podcast_title_setter(my_podcast):
    my_podcast.title = "Dark Throne"
    assert my_podcast.title == 'Dark Throne'

    with pytest.raises(ValueError):
        my_podcast.title = " "

    with pytest.raises(ValueError):
        my_podcast.title = ""


def test_podcast_eq():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 == podcast1
    assert podcast1 != podcast2
    assert podcast2 != podcast3


def test_podcast_hash():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    podcast_set = {podcast1, podcast2, podcast3}
    assert len(podcast_set) == 2  # Since podcast1 and podcast2 have the same ID


def test_podcast_lt():
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(200, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    assert podcast1 < podcast2
    assert podcast2 > podcast3
    assert podcast3 > podcast1


def test_user_initialization():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert repr(user1) == "<User 1: shyamli>"
    assert repr(user2) == "<User 2: asma>"
    assert repr(user3) == "<User 3: jenny>"
    assert user2.password == "pw67890"
    with pytest.raises(ValueError):
        user4 = User(4, "xyz  ", "")
    with pytest.raises(ValueError):
        user4 = User(5, "    ", "qwerty12345")


def test_user_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user4 = User(1, "Shyamli", "pw12345")
    assert user1 == user4
    assert user1 != user2
    assert user2 != user3


def test_user_hash():
    user1 = User(1, "   Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    user_set = set()
    user_set.add(user1)
    user_set.add(user2)
    user_set.add(user3)
    assert sorted(user_set) == [user1, user2, user3]
    user_set.discard(user1)
    user_set.discard(user2)
    assert list(user_set) == [user3]


def test_user_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "JeNNy  ", "pw87465")
    assert user1 < user2
    assert user2 < user3
    assert user3 > user1
    user_list = [user3, user2, user1]
    assert sorted(user_list) == [user1, user2, user3]


def test_user_add_remove_favourite_podcasts(my_user, my_subscription):
    my_user.add_subscription(my_subscription)
    assert repr(my_user.subscription_list[1]) == "<PodcastSubscription 1: Owned by shyamli>"
    my_user.add_subscription(my_subscription)
    assert len(my_user.subscription_list) == 2


def test_podcast_subscription_initialization(my_subscription):
    assert my_subscription.id == 1
    assert repr(my_subscription.owner) == "<User 1: shyamli>"
    assert repr(my_subscription.podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"

    assert repr(my_subscription) == "<PodcastSubscription 1: Owned by shyamli>"


def test_podcast_subscription_set_owner(my_subscription):
    new_user = User(2, "asma", "pw67890")
    my_subscription.owner = new_user
    assert my_subscription.owner == new_user

    with pytest.raises(TypeError):
        my_subscription.owner = "not a user"


def test_podcast_subscription_set_podcast(my_subscription):
    author2 = Author(2, "Author C")
    new_podcast = Podcast(200, author2, "Voices in AI")
    my_subscription.podcast = new_podcast
    assert my_subscription.podcast == new_podcast

    with pytest.raises(TypeError):
        my_subscription.podcast = "not a podcast"


def test_podcast_subscription_equality(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub3 = PodcastSubscription(2, my_user, my_podcast)
    assert sub1 == sub2
    assert sub1 != sub3


def test_podcast_subscription_hash(my_user, my_podcast):
    sub1 = PodcastSubscription(1, my_user, my_podcast)
    sub2 = PodcastSubscription(1, my_user, my_podcast)
    sub_set = {sub1, sub2}  # Should only contain one element since hash should be the same
    assert len(sub_set) == 1

# TODO : Write Unit Tests for CSVDataReader, Episode, Review, playlist classes

@pytest.fixture
def my_episode():
    return Episode("Episode 182 - Lyrically Weak", 2347, "This is about dogs", "2017-12-01 00:09:47+00", 
                   2, "http://reallifeactor.podomatic.com/enclosure/2017-11-30T19_09_56-08_00.mp3", 323)

def test_episode_initialisation(my_episode):
    assert my_episode._episode_name == "Episode 182 - Lyrically Weak"
    assert my_episode._episode_length == 2347
    assert my_episode._episode_description == "This is about dogs"
    assert my_episode._publication_date == "2017-12-01 00:09:47+00"
    assert my_episode._episode_id == 2
    assert my_episode._link_to_audio == "http://reallifeactor.podomatic.com/enclosure/2017-11-30T19_09_56-08_00.mp3"
    assert my_episode.podcast_id == 323
    
def test_episode_name_setter(my_episode):
    my_episode._episode_name = "Hello Bob"
    assert my_episode._episode_name == "Hello Bob"
    
def test_episode_description_setter(my_episode):
    my_episode._episode_description = "Hello Bob"
    assert my_episode._episode_description == "Hello Bob"
    
def test_episode_repr(my_episode):
    assert repr(my_episode) == "<Episode Episode 182 - Lyrically Weak: This is about dogs: 2017-12-01 00:09:47+00>"
    
def test_episode_eq():
    episode1 = Episode("Episode Name 1", 1234, "Description 1", "1/1/2002", 1, "www.google.com", 343)
    episode2 = Episode("Episode Name 2", 4352, "Description 2", "1/3/2222", 2, "www.google.com", 255)
    episode3 = Episode("Episode Name 1", 1234, "Description 1", "1/1/2002", 1, "www.google.com", 343)
    assert episode1 == episode3
    assert episode1 != episode2
    assert episode2 != episode3
    assert episode3 == episode1
    
def test_episode_lt():
    episode1 = Episode("Episode Name 1", 1234, "Description 1", "1/1/2002", 1, "www.google.com", 343)
    episode2 = Episode("Episode Name 2", 4352, "Description 2", "1/3/2022", 2, "www.google.com", 255)
    episode3 = Episode("Episode Name 3", 3421, "Description 3", "1/5/3022", 3, "www.google.com", 775)
    assert episode1 < episode2
    assert episode3 > episode1
    assert episode2 > episode1
    assert episode1 < episode3
    
def test_episode_hash():
    episodes = set()
    episode1 = Episode("Episode Name 1", 1234, "Description 1", "1/1/2002", 1, "www.google.com", 343)
    episode2 = Episode("Episode Name 2", 4352, "Description 2", "1/3/2022", 2, "www.google.com", 255)
    episode3 = Episode("Episode Name 3", 3421, "Description 3", "1/5/3022", 3, "www.google.com", 775)
    episodes.add(episode1)
    episodes.add(episode2)
    episodes.add(episode3)
    assert len(episodes) == 3
    assert repr(sorted(episodes)) == "[<Episode Episode Name 1: Description 1: 1/1/2002>, <Episode Episode Name 2: Description 2: 1/3/2022>, <Episode Episode Name 3: Description 3: 1/5/3022>]"
    
    
@pytest.fixture
def my_review(my_podcast, my_user):
    return Review(1, my_podcast, my_user, 5, "Review 1")

def test_review_initialisation(my_review):
    assert my_review.review_id == 1
    assert repr(my_review.reviewed_podcast) == "<Podcast 100: 'Joe Toste Podcast - Sales Training Expert' by Joe Toste>"
    assert repr(my_review.user_review) == "<User 1: shyamli>"
    assert my_review.user_rating == 5
    assert my_review.review_content == "Review 1"
    
def test_user_rating_setter(my_review):
    my_review.user_rating = 4
    assert my_review.user_rating == 4
    
def test_review_content_setter(my_review):
    my_review.review_content = "Review 2"
    assert my_review.review_content == "Review 2"
    
def test_review_repr(my_review):
    assert repr(my_review) == "<Review 1: shyamli gave a rating of 5 on 'Joe Toste Podcast - Sales Training Expert'>"
    
def test_review_eq():
    review1 = Review(1, my_podcast, my_user, 5, "Review 1")
    review2 = Review(2, my_podcast, my_user, 4, "Review 2")
    review3 = Review(1, my_podcast, my_user, 3, "Review 3")
    assert review1 == review3
    assert review2 == review2
    assert review3 != review2
    
def test_review_lt():
    review1 = Review(1, my_podcast, my_user, 5, "Review 1")
    review2 = Review(3, my_podcast, my_user, 4, "Review 2")
    review3 = Review(10, my_podcast, my_user, 3, "Review 3")
    assert review1 < review3
    assert review2 > review1
    assert review3 > review1
    
def test_review_hash(my_user):
    reviews = set()
    author1 = Author(1, "Author A")
    author2 = Author(2, "Author C")
    author3 = Author(3, "Author B")
    podcast1 = Podcast(100, author1, "Joe Toste Podcast - Sales Training Expert")
    podcast2 = Podcast(100, author2, "Voices in AI")
    podcast3 = Podcast(101, author3, "Law Talk")
    review1 = Review(1, podcast1, my_user, 5, "Review 1")
    review2 = Review(3, podcast2, my_user, 4, "Review 2")
    review3 = Review(10, podcast3, my_user, 3, "Review 3")
    reviews.add(review1)
    reviews.add(review2)
    reviews.add(review3)
    assert len(reviews) == 3
    assert sorted(reviews) == [review1, review2, review3]
    assert repr(reviews) == "{<Review 10: shyamli gave a rating of 3 on 'Law Talk'>, <Review 3: shyamli gave a rating of 4 on 'Voices in AI'>, <Review 1: shyamli gave a rating of 5 on 'Joe Toste Podcast - Sales Training Expert'>}"
    
@pytest.fixture
def my_playlist(my_user):
    return Playlist(1, my_user, "playlist 1")

def test_playlist_initialisation(my_playlist, my_user):
    assert my_playlist.playlist_id == 1
    assert my_playlist.playlist_user == my_user
    assert my_playlist.playlist_name == "playlist 1"
    
def test_playlist_name_setter(my_playlist):
    my_playlist.playlist_name = "playlist 2"
    assert my_playlist.playlist_name == "playlist 2"
    
def test_playlist_add_episode(my_playlist):
    episode1 = Episode("Episode Name 1", 1234, "Description 1", "1/1/2002", 1, "www.google.com", 343)
    episode2 = Episode("Episode Name 2", 4352, "Description 2", "1/3/2022", 2, "www.google.com", 255)
    episode3 = Episode("Episode Name 3", 3421, "Description 3", "1/5/3022", 3, "www.google.com", 775)
    my_playlist.add_episode(episode1)
    my_playlist.add_episode(episode2)
    my_playlist.add_episode(episode3)
    
    with pytest.raises(TypeError):
        my_playlist.add_episode("episode1")
    
    assert repr(my_playlist.episode_list) == "[<Episode Episode Name 1: Description 1: 1/1/2002>, <Episode Episode Name 2: Description 2: 1/3/2022>, <Episode Episode Name 3: Description 3: 1/5/3022>]"
    
def test_playlist_remove_episode(my_playlist):
    episode1 = Episode("Episode Name 1", 1234, "Description 1", "1/1/2002", 1, "www.google.com", 343)
    episode2 = Episode("Episode Name 2", 4352, "Description 2", "1/3/2022", 2, "www.google.com", 255)
    my_playlist.add_episode(episode1)
    my_playlist.add_episode(episode2)
    my_playlist.remove_episode(episode1)
    
    with pytest.raises(IndexError):
        my_playlist.remove_episode(episode1)
        
    assert repr(my_playlist.episode_list) == "[<Episode Episode Name 2: Description 2: 1/3/2022>]"
    
def test_playlist_eq():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    playlist1 = Playlist(1, user1, "playlist 1")
    playlist2 = Playlist(2, user2, "playlist 2")
    playlist3 = Playlist(1, user1, "playlist 1")
    assert playlist1 == playlist3
    assert playlist2 != playlist3
    assert playlist1 != playlist2
    assert playlist3 == playlist3
    
def test_playlist_lt():
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "Melody", "pw3892482")
    playlist1 = Playlist(1, user1, "playlist 1")
    playlist2 = Playlist(2, user2, "playlist 2")
    playlist3 = Playlist(3, user3, "playlist 3")
    assert playlist3 > playlist1
    assert playlist2 < playlist3
    assert playlist1 < playlist2
    
def test_playlist_hash():
    playlists = set()
    user1 = User(1, "Shyamli", "pw12345")
    user2 = User(2, "asma", "pw67890")
    user3 = User(3, "Melody", "pw3892482")
    playlist1 = Playlist(1, user1, "playlist 1")
    playlist2 = Playlist(2, user2, "playlist 2")
    playlist3 = Playlist(3, user3, "playlist 3")
    playlists.add(playlist1)
    playlists.add(playlist2)
    playlists.add(playlist3)
    assert len(playlists) == 3
    assert repr(sorted(playlists)) == "[<Playlist 1: playlist 1 by shyamli>, <Playlist 2: playlist 2 by asma>, <Playlist 3: playlist 3 by melody>]"

@pytest.fixture
def my_csv_reader():
    # Initialising CSVDataReader object
    reader = CSVDataReader(Path('podcast') / 'adapters' / 'data')
    reader.create_podcast()
    reader.load_episodes_into_podcasts()
    return reader

@pytest.fixture
def my_csv_podcast_1(my_csv_reader):
    # Pulling one instance of the podcast object from the CSVData that has no episodes
    return my_csv_reader.podcast_list[0]

@pytest.fixture
def my_csv_podcast_2(my_csv_reader):
    # Pulling one instance of the podcast object from the CSVData that has episodes
    return my_csv_reader.podcast_list[4]
    
def test_create_author(my_csv_reader):
    author = Author(my_csv_reader.author_id, "name")
    assert isinstance(author, Author)
    assert author.name == "name"
    assert repr(author) == "<Author 1123: name>" #Its 982 diff authors in the CSV file but +1 for "name".

def test_create_category(my_csv_reader):
    cat = Category(CSVDataReader.category_id, "name")
    assert isinstance(cat, Category)
    assert cat.name == "name"
    assert repr(cat) == "<Category 4583: name>" #Its 2166 diff categories in the CSv file but +1 for "name".


def test_csv_reader_podcast(my_csv_reader):
    
    # Testing correct types for the list and the Podcast object
    assert repr(type(my_csv_reader.podcast_list)) == "<class 'list'>"
    assert repr(type(my_csv_reader.podcast_list[1])) == "<class 'podcast.domainmodel.model.Podcast'>"

    # Testing to see podcast object output
    assert repr(my_csv_reader.podcast_list[1]) == "<Podcast 3: 'Onde Road - Radio Popolare' by Radio Popolare>"
    
def test_csv_reader_podcast_attributes(my_csv_reader, my_csv_podcast_1, my_csv_podcast_2):
    
    # Testing for the attributes from the Podcast object that was listed in the memory_repo
    assert my_csv_podcast_1.id == 2
    assert repr(my_csv_podcast_1.author) == "<Author 1: Brian Denny>"
    assert repr(type(my_csv_podcast_1.author)) == "<class 'podcast.domainmodel.model.Author'>"
    assert my_csv_podcast_1.title == "Brian Denny Radio"
    assert my_csv_podcast_1.image == "http://is5.mzstatic.com/image/thumb/Music111/v4/49/c8/19/49c8190a-ca0f-f32c-c089-d7ae502d2cb8/source/600x600bb.jpg"
    assert my_csv_podcast_1.language == "English"
    assert repr(my_csv_podcast_1.categories[0]) == "<Category 1: Professional>"
    assert repr(type(my_csv_podcast_1.categories[0])) == "<class 'podcast.domainmodel.model.Category'>"
    assert repr(my_csv_podcast_1.episodes[0].episode_name) == "'TRUMPMANIA - Lavie Margolin talks about his book'"
    
    # Testing for podcasts that do have episodes
    assert my_csv_podcast_2.title == "Mike Safo"
    assert my_csv_podcast_2.episodes == []
