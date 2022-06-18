build: 
	docker build app/. -t tupperward/butterbean

app: db
	docker compose up -d app

db:
	docker compose up -d db

stop:
	docker compose down

reset: stop
	docker compose up -d

rerun: stop build
	docker compose up -d

clean:
	docker compose kill
	docker system prune -f