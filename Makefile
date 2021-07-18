check_env:
	test -f .env || cp .env.sample .env

dev: check_env
	docker-compose up -d --build

shell: check_env
	docker-compose run --rm api bash

attach: dev
	docker-compose exec api bash
