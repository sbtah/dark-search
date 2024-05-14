# Dark Search
## Q: what is it?: An async Tor domain search service.

Welcome to the Dark Search!

This is a python based crawler service. Project was built with Django, Celery and asyncio. Its main purpose is to search for Tor domains while providing information and statistics about them.
Current focus is to find and identify and compare domains with content related to: hacking, ransomware, data bases, leaked credentials etc.

### Current state:
- The project is being redesigned. Previous working version is on `archived` branch.

## Features
- Crawl specified webpage,
- Filter urls,
- Schedule crawl tasks for newly found domains.


## Installation

To set up this project locally, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/sbtah/dark-search.git
cd dark-search
```

2. Build Images:
```bash
docker compose build
docker compose up
```

3. Current start method:
 - Just start the containers...


4. Create super user for scout service.
```bash
docker exec -it search /bin/sh
python3 manage.py createsuperuser
```

5. Navigate to: `http://localhost:9002/admin`
 - Here you will see crawling Tasks.


6. Create super user for api service.
```bash
docker exec -it api /bin/sh
python3 manage.py createsuperuser
```

7. Navigate to: `http://localhost:9003/admin`
 - Here you will see your crawled data. Enjoy!
