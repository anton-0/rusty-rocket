start:
	[ ! -f .env ] && cp .env.example .env
	docker compose up -d
	chmod +x healthcheck.sh
	./healthcheck.sh
	docker exec -it library-api alembic upgrade head

stop:
	docker compose down --volumes