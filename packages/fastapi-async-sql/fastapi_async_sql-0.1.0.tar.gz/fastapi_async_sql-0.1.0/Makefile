.PHONY: migrations

lint:
	uv run pre-commit install
	uv run pre-commit run -a -v

update:
	uv lock --upgrade
	uv run pre-commit autoupdate -j 10

sync:
	uv sync --all-extras

lock:
	uv lock

test:
	uv run pytest -vvv

test-cov:
	uv run pytest -vvv --cov=src --cov-report=term-missing --cov-report=html

clean:
	@find . -name '*.pyc' -exec rm -rf {} +
	@find . -name '__pycache__' -exec rm -rf {} +
	@find . -name 'Thumbs.db' -exec rm -rf {} +
	@find . -name '*~' -exec rm -rf {} +
	@find . -name '.coverage' -exec rm -f {} +
	@rm -rf .cache
	@rm -rf build
	@rm -rf dist
	@rm -rf *.egg-info
	@rm -rf htmlcov
	@rm -rf .tox/
	@rm -rf docs/_build
	@rm -rf .mypy_cache
	@rm -rf .pytest_cache
