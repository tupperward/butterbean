start: restore backup app

build: 
	docker compose build app restore backup --no-cache

restore: db pause
	docker compose up -d restore

backup: db
	docker compose up -d backup

app: db pause
	docker compose up -d app

db:
	docker compose up -d db

stop:
	docker compose down

pause:
	sleep 15

clean:
	docker compose kill
	docker system prune -f