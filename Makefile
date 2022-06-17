build: 
	docker compose build --no-cache

backup: db
	docker compose up -d backup

app: db 
	docker compose up -d app

db:
	docker compose up -d db
	sleep 5

stop:
	docker compose down

reset: stop build start

exec:
	docker compose exec db bin/bash

dblogs:
	docker compose logs db

applogs:
	docker compose logs app

clean:
	docker compose kill
	docker system prune -f