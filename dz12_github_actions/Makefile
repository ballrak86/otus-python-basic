lint:
	poetry run pylint $(git ls-files '*.py')

test:
	poetry run pytest

coverage:
	poetry run pytest -s --cov --cov-report html --cov-fail-under 86

coveralls:
	poetry run coverage run --source=mypkg -m pytest tests coveralls