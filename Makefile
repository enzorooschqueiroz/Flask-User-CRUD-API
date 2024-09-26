APP = restapi

test:
	@flake8 . --exclude .venve

compose:
	@docker compose build
	@docker compose up