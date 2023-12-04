.EXPORT_ALL_VARIABLES:

export COMPOSE_DOCKER_CLI_BUILD=1
export DOCKER_BUILDKIT=1

include .env
export $(shell sed 's/=.*//' .env)

test:
	pytest --cov=./src/tests --cov-report=xml -s -vv

analise-estatica:
	black .
	isort . --profile black
	flake8 .
	bandit .
	safety check

docker-down:
	docker compose down --remove-orphans

docker-up: docker-down
	docker compose up -d --build --remove-orphans

docker-analise-estatica: docker-up
	docker compose run \
		--rm \
		--no-deps \
		--user 1000:1000 \
		--entrypoint="make analise-estatica" \
		api

docker-test: docker-up
	docker compose run \
		--rm \
		--no-deps \
		--user 1000:1000 \
		--entrypoint="make test" \
		api
