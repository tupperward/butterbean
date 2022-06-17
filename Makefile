build: 
	docker compose build --no-cache

backup: db
	docker compose up -d backup

app: db
	sleep 8
	docker compose up -d app

db:
	docker compose up -d db

stop:
	docker compose down

reset: stop build start

clean:
	docker compose kill
	docker system prune -f