# Dark Search
## Q: what is it?: An async Tor domain search service.

Welcome to Dark Search!

Dark Search is a sophisticated Python-based search engine designed to delve into the depths of the internet. 
Crafted using: Django, Django-Ninja, pydantic, Celery, Redis, postgresql, asyncio and tested with pytest and mypy.
This project is dedicated to unearthing Tor(onion) domains,
while furnishing comprehensive information and insightful statistics about them.

At its core, Dark Search is engineered to locate, identify and analyze domains associated with various facets of the darker side of the internet.
Including but not limited to hacking, ransomware, databases, leaked credentials, and more.

### Current state:
- The project is being redesigned. Previous working (POC) version is on `archived` branch.

![alt text](https://github.com/sbtah/dark-search/blob/main/1.png?raw=true)
----
## Working features:
- Crawl specified webpage,
- Send data to API service,
- Extract, filter and validate urls on each crawled webpage,
- Retry requests for urls without response,
- Schedule crawl tasks for newly found domains,

## WIP:
- Save extensive data about crawled webpage,
- Translate text content and extract text meaning(AI),
- Show all kinds of statistics in dedicated front app,

## Installation:
To set up this project locally, follow these steps:

- Clone the repository:
```bash
git clone https://github.com/sbtah/dark-search.git
cd dark-search
```

- Build Images:
```bash
make build
```

- Start services:
```bash
make run
```

- Run a CrawlTask
```bash
make run-crawl-task
```

- Navigate to: `http://localhost:9002/admin`
   - Here you will see crawling Tasks.
   - login: `admin`
   - password: `admin`

- Navigate to: `http://localhost:9003/admin`
  - Here you will see your crawled data. Enjoy!
  - login: `admin`
  - password: `admin`

- Navigate to: `http://localhost:5559`
   - Here you can debug your Celery crawling tasks.

- Navigate to: `http://localhost:5558`
   - Here you can debug your API processing tasks.

- Navigate to: `http://localhost:9003/api/docs`
   - API Documentation.

- Navigate to: `http://localhost:3000`
   - Dedicated front application.

![alt text](https://github.com/sbtah/dark-search/blob/main/2.png?raw=true)
