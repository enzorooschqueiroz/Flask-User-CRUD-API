APP = restapi

test:
	@black .
	@pytest -v --disable-warnings

compose:
	@docker-compose build
	@docker-compose up