lint:
	docker compose exec api ruff check /app/app

lint-fix:
	docker compose exec api ruff check /app/app --fix

format:
	docker compose exec api ruff format /app/app

check:
	docker compose exec api ruff check /app/app
	docker compose exec api ruff format /app/app --check
