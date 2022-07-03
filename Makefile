stop:
	docker compose down

reset: stop
	docker compose up -d --build

exec:
	docker compose exec db bin/bash

applogs:
	docker compose logs app

clean:
	docker compose kill
	docker system prune -f