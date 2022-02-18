VERSION := `python VERSION`

.PHONY: login build-syft push-syft build-domain push-domain build-notebook push-notebook domain-dev-up domain-dev-down domain-dev-logs domain-prod-up domain-prod-down domain-prod-logs db-admin notebook

login:
	docker login

build-syft:
	docker build \
	  -f docker/syft.Dockerfile \
	  --build-arg GPU=false \
	  -t wicrep/syft:latest \
	  -t wicrep/syft:$(VERSION) \
	  .

push-syft:
	docker push -a wicrep/syft

build-domain:
	docker build \
	  -f docker/grid.Dockerfile \
	  --build-arg APP=domain \
	  --build-arg APP_ENV=production \
	  --build-arg VERSION=$(VERSION) \
	  -t wicrep/grid-domain:latest \
	  -t wicrep/grid-domain:$(VERSION) \
	  .

push-domain:
	docker push -a wicrep/grid-domain

build-notebook:
	docker build \
	  -f docker/notebook.Dockerfile \
	  -t wicrep/syft-notebook:latest \
	  -t wicrep/syft-notebook:$(VERSION) \
	  .

push-notebook:
	docker push -a wicrep/syft-notebook

domain-dev-up:
	docker-compose -f ./docker/docker-compose.domain.dev.yml up -d

domain-dev-down:
	docker-compose -f ./docker/docker-compose.domain.dev.yml down

domain-dev-logs:
	docker-compose -f ./docker/docker-compose.domain.dev.yml logs -f

domain-prod-up:
	docker-compose -f ./docker/docker-compose.domain.prod.yml up -d

domain-prod-down:
	docker-compose -f ./docker/docker-compose.domain.prod.yml down

domain-prod-logs:
	docker-compose -f ./docker/docker-compose.domain.prod.yml logs -f

db-admin:
	PGPASSWORD=dbpass pgcli -h localhost -p 5432 -U postgres -d domain

notebook:
	docker run -it --rm \
	  -p 8888:8888 \
	  -v "`pwd`/packages/syft/examples:/notebook" \
	  --network local-grid \
	  wicrep/syft-notebook
