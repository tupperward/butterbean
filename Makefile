start: restore app

build: 
	docker compose build app restore backup --no-cache

restore: db
	sleep 5
	docker compose up -d restore

backup: db
	docker compose up -d backup

app: db
	sleep 5
	docker compose up -d app

db:
	docker compose up -d db

stop:
	docker compose down

reset: stop build start

clean:
	docker compose kill
	docker system prune -f