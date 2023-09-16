# Tor Scout. 
## what is it? : Tor domain search service.


Welcome to the Tor Scout!
This is a python-asyncio crawler service/project. Built with Django and Celery, it allows users to search for Tor domains while providing information and statistics about them.
Current focus is to find and identify domains with content related to: Hacking, data bases, selling credentials etc.

## Features

### Done:
- Crawl tor domain and find new domains to crawl in process.
- Display detailed information about each domain, including its title, description, and last update.
- Automated launching of crawlers using Celery.

### WIP:
- User-friendly web interface for easy interaction.
- Customizable and extensible codebase for further development.

## Installation

To set up this project locally, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/yourusername/tor-domain-search.git
cd tor-domain-search
```

2. Build Images:
```bash
docker compose build
docker compose up
```

3. Create super user for scout service.
```bash
docker exec -it tor-scout /bin/sh
python3 manage.py createsuperuser
```

4. Navigate to: `http://localhost:9002/admin`
 - Create a TOR domain
 - Create related Task.

5. Current start method:
 - Just watch the logs. Tasks are scheduled each 5 seconds.

6. Create super user for scout service.
```bash
docker exec -it tor-scout-api /bin/sh
python3 manage.py createsuperuser
```

7. Navigate to: `http://localhost:9003/admin`
 - Enjoy.
