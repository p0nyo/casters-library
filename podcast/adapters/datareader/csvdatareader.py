import csv
import os
from pathlib import Path

from podcast.domainmodel.model import Podcast, Episode, Author, Category


#Function will return the key for the value
def get_key_for_value(dict):
    temp_id = 0
    for key, auth_obj in dict.items():
        if auth_obj.id == temp_id:
            return temp_id
        temp_id += 1


class CSVDataReader:
    """class variable not associated with any one instance of the class.
        These static variables are used as temporary memory."""
    author_id = 1
    category_id = 1
    category_dict = dict()
    author_dict = dict()
    podcast_list = list()
    episode_list = list()

    def __init__(self, data_pathway: str):
        if os.environ.get('REPOSITORY') == 'Database':
            if os.environ.get('TESTING') == 'True':
                self.podcast_csv_pathway = data_pathway  + '/test_data' + '/podcasts.csv'
                self.episodes_csv_pathway = data_pathway + '/test_data' + '/episodes.csv'
            elif os.environ.get('TESTING') == 'False':
                self.podcast_csv_pathway = data_pathway + '/adapters' + '/data' + '/podcasts.csv'
                self.episodes_csv_pathway = data_pathway + '/adapters' + '/data' + '/episodes.csv'
        elif os.environ.get('REPOSITORY') == 'Memory':
            self.podcast_csv_pathway = data_pathway / 'podcasts.csv'
            self.episodes_csv_pathway = data_pathway / 'episodes.csv'

    def read_csv(self, file_pathway: str):
        with open(file_pathway) as csv_file:
            csv_reader = csv.reader(csv_file)
            header = next(csv_reader)

            for row in csv_reader:
                row = [item.strip() for item in row]
                yield row

    # Create Author first before and add their podcasts
    def create_author(self, author_name: str) -> int:

        # Will add author to CSVDataReader.author_dict if not already present
        if author_name not in CSVDataReader.author_dict.values():
            author_obj = Author(CSVDataReader.author_id, author_name)
            CSVDataReader.author_dict[CSVDataReader.author_id] = author_obj
            CSVDataReader.author_id += 1

            # Will return the ID of the added author.
            return CSVDataReader.author_id - 1

        # if present will return the ID of the author.
        return get_key_for_value(CSVDataReader.author_dict, author_name)

    # Need to create category object before creating podcast
    def create_category(self, category_name: str) -> int:
        if category_name not in CSVDataReader.category_dict.values():
            category_obj = Category(CSVDataReader.category_id, category_name)
            CSVDataReader.category_dict[CSVDataReader.category_id] = category_obj
            CSVDataReader.category_id += 1

            return CSVDataReader.category_id - 1

        return get_key_for_value(CSVDataReader.category_dict, category_name)

    def create_podcast(self):

        for row in self.read_csv(self.podcast_csv_pathway):

            try:
                # Unpack all the information in each row of CSV file
                podcast_id = int(row[0])
                title = str(row[1])
                image = str(row[2])
                description = str(row[3])
                language = str(row[4])
                categories = str(row[5])
                website = str(row[6])
                author_name = str(row[7].strip())
                itunes_id = int(row[8])

                #Will call the create_author function and return the ID of the author in CSVDataReader.author_dict
                author_id: int = self.create_author(author_name)

            # If Row does not have the correct format or missing information then it will be skipped
            except:
                pass

            else:
                podcast = Podcast(podcast_id, CSVDataReader.author_dict[author_id],
                                  title, image, description, website, itunes_id, language)

                # Will call the create_category function and return the ID of the category in CSVDataReader.category_dict
                for category in categories.split("|"):
                    # If category does not exist then it will be created
                    category_id: int = self.create_category(category.strip())
                    podcast.add_category(CSVDataReader.category_dict[category_id])

                # Will add the podcast to the author object
                CSVDataReader.author_dict[author_id].add_podcast(podcast)

                #Will add the podcast to the podcast list and sort the podcast list based on title
                (CSVDataReader.podcast_list.append(podcast))

        """    if len(CSVDataReader.podcast_list) > 4:
                    CSVDataReader.podcast_list.sort()"""

    def load_episodes_into_podcasts(self):

        for row in self.read_csv(self.episodes_csv_pathway):

            try:
                #Unpacking each row of information
                episode_id = int(row[0])
                podcast_id = int(row[1])
                title = str(row[2])
                link_to_audio = str(row[3])
                audio_length = str(row[4])
                description = str(row[5])
                publication_data = str(row[6])

            #Will pass the row if the formate is improper
            except:
                pass

            else:
                #Creating episode class with unpacked values
                episode = Episode(title, audio_length, description, publication_data,
                                  episode_id, link_to_audio, podcast_id)

                #Episodes lists which is used to populate the database
                CSVDataReader.episode_list.append(episode)

                #Finds the index of podcast and adds the episode into the podcast episodes
                for podcast in CSVDataReader.podcast_list:
                    if podcast._id == podcast_id:
                        podcast_index = CSVDataReader.podcast_list.index(podcast)

                """Adds the episode to the corresponding podcast in the CSVDataReader.podcast_list
                and sorts the episodes list in ascending order of episode_id"""
                (CSVDataReader.podcast_list[podcast_index]).add_episode(episode)
                CSVDataReader.podcast_list[podcast_index].get_episodes.sort()
