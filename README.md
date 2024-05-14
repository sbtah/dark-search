# Dark Search
## Q: what is it?: An async Tor domain search service.

Welcome to Dark Search!

Dark Search is a sophisticated Python-based crawler service designed to delve into the depths of the internet. Crafted using Django, Celery, and asyncio, this project is dedicated to unearthing Tor domains while furnishing comprehensive information and insightful statistics about them.

At its core, Dark Search is engineered to locate, identify, and analyze domains associated with various facets of the darker side of the internet, including but not limited to hacking, ransomware, databases, leaked credentials, and more.
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
