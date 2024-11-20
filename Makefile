APP = restapi

test:
	@black .
	@pytest -v --disable-warnings

compose:
	@docker-compose build
	@docker-compose up

setup-dev:
	@kind create cluster --config kubernetes/config/config.yaml
	@kubectl apply -f https://kind.sigs.k8s.io/examples/ingress/deploy-ingress-nginx.yaml
	@kubectl wait --namespace ingress-nginx \
		--for=condition=ready pod \
		--selector=app.kubernetes.io/component=controller \
		--timeout=270s

teardown-dev:
	@kind delete clusters kind