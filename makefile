init:
	aerich init -t config.db.TORTOISE_ORM
	aerich init-db

migrate:
	aerich upgrade

makemigrations:
	aerich migrate

clean:
	rm -rf migrations
	rm -f pyproject.toml

run:
	python main.py

build-docker:
	docker build -t monitoring:latest .

run-docker:
	echo "running docker"
	docker run --rm -p 8001:8000 --name monitoring -d monitoring:latest

stop-docker:
	echo "stop docker"
	docker stop -f monitoring

install:
	pip install -r requirements.txt