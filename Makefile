CMD=poetry run
MODULE=backend

dev:
	$(CMD) litestar --app $(MODULE).app:app run --debug --reload


prod:
	$(CMD) litestar --app $(MODULE).app:app run


test:
	$(CMD) pytest --cov-report term-missing --cov=$(MODULE)


lint:
	$(CMD) ruff check $(MODULE)


analysis:
	$(CMD) mypy $(MODULE)


clean:
	clear
	rm -rf *.sqlite
