"""
Utility script for removing local development databases and Django migrations.
"""
import os


CURRENT_DIR = os.getcwd()
API_CRAWLED_PATH = os.path.join(CURRENT_DIR, 'crawled/migrations')


DIRS_TO_CLEAN = [API_CRAWLED_PATH,]


print('Removing migrations for API service!')


for directory in DIRS_TO_CLEAN:
    files = os.listdir(directory)
    for file in files:
        if file == '__init__.py':
            continue
        file_path = os.path.join(directory, file)
        print(f'Removing file: {file_path}')
        os.remove(file_path)


print('Removing migrations for API service was finished!')
