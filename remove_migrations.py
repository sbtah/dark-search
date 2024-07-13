"""
Utility script for removing local development databases and Django migrations.
"""
import os
import time


CURRENT_DIR = os.getcwd()
SEARCH_PARAMS_PATH = os.path.join(CURRENT_DIR, 'search/parameters/migrations')
SEARCH_TASKS_PATH = os.path.join(CURRENT_DIR, 'search/tasks/migrations')
API_CRAWLED_PATH = os.path.join(CURRENT_DIR, 'api/crawled/migrations')
DIRS_TO_CLEAN = [SEARCH_TASKS_PATH, SEARCH_PARAMS_PATH, API_CRAWLED_PATH]


print('WARNING, This script will remove your migrations in 5 seconds...')
for _ in range(1, 6)[::-1]:
    print(_)
    time.sleep(1)


for directory in DIRS_TO_CLEAN:
    files = os.listdir(directory)
    for file in files:
        if file == '__init__.py':
            continue
        file_path = os.path.join(directory, file)
        os.remove(file_path)
