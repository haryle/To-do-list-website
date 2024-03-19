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


coverage:
	$(CMD) coverage xml -i


clean:
	clear
	rm -rf *.sqlite
	rm .coverage
	rm coverage.xml
