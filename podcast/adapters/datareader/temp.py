from podcast import CSVDataReader


def x():
    reader = CSVDataReader()
    reader.create_podcast()
    reader.load_episodes_into_podcasts()

    for podcast in CSVDataReader.podcast_list:
        print("\n\n")
        print(podcast)
        break

x()