build:
	docker compose build

run:
	docker compose up -d

stop:
	docker compose down -t 3

test-search:
	docker compose run --rm search sh -c 'pytest'

test-api:
	docker compose run --rm api sh -c 'pytest'

check-types-search:
	docker compose run --rm search sh -c 'mypy /search --explicit-package-bases'

check-linting-search:
	docker compose run --rm search sh -c 'flake8'

check-linting-api:
	docker compose run --rm api sh -c 'flake8'

run-crawl:
	@echo "Starting a CrawlTask..."
	@sleep 5
	docker compose run --rm search sh -c 'python manage.py crawl'

run-manual:
	@echo "Starting Manual crawling..."
	@sleep 5
	docker compose run --rm search sh -c 'python manage.py manual'


trash-local-databases:
	@echo "Warning this command will remove local databases!"
	@sleep 5
	sudo rm -rfv ./local/*
