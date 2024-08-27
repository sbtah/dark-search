build:
	docker compose build

run:
	docker compose up -d

run-front:
	docker compose -f docker-compose-front.yml up -d

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

run-probe:
	@echo "Starting a Probing spider..."
	@sleep 5
	@docker compose run --rm search sh -c 'python manage.py probe'

run-manual:
	@echo "Starting Manual crawling..."
	@sleep 5
	docker compose run --rm search sh -c 'python manage.py manual'

trash-api:
	@echo "Warning this command will remove local API volume!"
	@docker compose run --rm api sh -c 'python clear_migrations.py'
	@docker compose down
	@sleep 5
	@docker volume rm dark-search_api-db-dev

trash-search:
	@echo "Warning this command will remove local SEARCH volume!"
	@docker compose run --rm search sh -c 'python clear_migrations.py'
	@docker compose down
	@sleep 5
	@docker volume rm dark-search_search-db-dev

trash-redis:
	@echo "Warning this command will remove local REDIS volume!"
	@docker compose down
	@sleep 5
	@docker volume rm dark-search_redis-dev

trash-volumes:
	@echo "Warning this command will remove ALL local volumes!"
	@docker compose run --rm api sh -c 'python clear_migrations.py'
	@docker compose run --rm search sh -c 'python clear_migrations.py'
	@docker compose down
	@sleep 5
	@docker volume rm $(shell docker volume ls --format '{{ .Name }}' | grep -E "dark-search_")
