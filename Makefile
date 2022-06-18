build: 
	docker build app/. -t tupperward/butterbean

app: db
	docker compose up -d app

db:
	docker compose up -d db
	sleep 5

stop:
	docker compose down

reset: stop
	docker compose up -d

rerun: stop build
	docker compose up -d

exec:
	docker compose exec db bin/bash

dblogs:
	docker compose logs db

applogs:
	docker compose logs app

clean:
	docker compose kill
	docker system prune -f