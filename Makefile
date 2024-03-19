
dev:
	poetry  run litestar --app backend.app:app run --debug --reload


prod:
	poetry run litestar --app backend.app:app run


test:
	poetry run pytest


clean:
	rm -rf *.sqlite