# Dark Search
## Q: what is it?: An asyncio Tor domain search service.

Welcome to Dark Search!

Dark Search is a sophisticated Python-based crawler service designed to delve into the depths of the internet. 
Crafted using Django, Celery, Redis, postgresql, asyncio and tested with pytest.
This project is dedicated to unearthing Tor(onion) domains,
while furnishing comprehensive information and insightful statistics about them.

At its core, Dark Search is engineered to locate, identify and analyze domains associated with various facets of the darker side of the internet.
Including but not limited to hacking, ransomware, databases, leaked credentials, and more.

### Current state:
- The project is being redesigned. Previous working (POC) version is on `archived` branch.
- The main Crawler class is finished!
- The Task model is ready.
- Almost all tests for search service components are ready.


![alt text](https://github.com/sbtah/dark-search/blob/main/1.png?raw=true)
----
## Features:
- Crawl specified webpage,
- Extract, filter and validate urls on each crawled webpage,
- Retry requests for urls without response,
- Schedule crawl tasks for newly found domains,
- Save extensive data about crawled webpage.

## Installation:
To set up this project locally, follow these steps:

1. Clone the repository:
```bash
git clone https://github.com/sbtah/dark-search.git
cd dark-search
```

2. Build Images:
```bash
make build
```

3. Start services:
```bash
make run
```

3. Run a CrawlTask
```bash
make run-crawl-task
```

5. Navigate to: `http://localhost:9002/admin`
 - Here you will see crawling Tasks.

6. Navigate to: `http://localhost:9003/admin`
 - Here you will see your crawled data. Enjoy!

7. Navigate to: `http://localhost:5559`
 - Here you can debug your Celery crawling tasks.

7. Navigate to: `http://localhost:5558`
 - Here you can debug your API processing tasks.

7. Navigate to: `http://localhost:9003/api/docs`
 - API Documentation.

![alt text](https://github.com/sbtah/dark-search/blob/main/2.png?raw=true)
