CMD=poetry run
MODULE=backend

install:
	poetry install

dev:
	$(CMD) litestar --app $(MODULE).app:app run --debug --reload


prod:
	$(CMD) litestar --app $(MODULE).app:app run


test:
	$(CMD) pytest tests 	--cov=$(MODULE)


lint:
	$(CMD) ruff check $(MODULE)


analysis:
	$(CMD) mypy $(MODULE)


clean:
	clear
	rm -rf *.sqlite
