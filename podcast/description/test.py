# import podcast.adapters.repository as repo
# from podcast.adapters.memory_repository import MemoryRepository, populate
#
#
# repo.repo_instance = MemoryRepository()
# populate(repo.repo_instance)
#
# podcast = repo.repo_instance.get_podcast()
# p1 = podcast[1]
# print(type(podcast))
# print(p1)
# print(p1.get_categories)
# for category in p1.get_categories:
#     print(category)