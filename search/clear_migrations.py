"""
Utility script for removing local development databases and Django migrations.
"""
import os


CURRENT_DIR = os.getcwd()
SEARCH_PARAMS_PATH = os.path.join(CURRENT_DIR, 'parameters/migrations')
SEARCH_TASKS_PATH = os.path.join(CURRENT_DIR, 'tasks/migrations')


DIRS_TO_CLEAN = [SEARCH_TASKS_PATH, SEARCH_PARAMS_PATH]


print('Removing migrations for SEARCH service!')


for directory in DIRS_TO_CLEAN:
    files = os.listdir(directory)
    for file in files:
        if file == '__init__.py':
            continue
        file_path = os.path.join(directory, file)
        print(f'Removing file: {file_path}')
        os.remove(file_path)


print('Removing migrations for SEARCH service was finished!')
