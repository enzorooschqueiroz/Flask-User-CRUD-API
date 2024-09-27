APP = restapi

test:
	@flake8 . --exclude .venve
	@pytest -v --disable-warnings

compose:
	@docker compose build
	@docker compose up