dev_compose_file = docker-compose.yml
# test_compose_file = docker-compose.test.yml

up: $(dev_compose_file)
	@echo "Building and starting up containers..."
	docker-compose -f $(dev_compose_file) up -d --build

down: $(dev_compose_file)
	@echo "Stopping and removing containers, networks, volume..."
	docker-compose -f $(dev_compose_file) down

restart: $(dev_compose_file)
	docker-compose -f $(dev_compose_file) down
	@echo "Cleaning volumes"
	docker system prune --volumes -f
	rm -rf docker/volumes/vol_mysql
	docker-compose -f $(dev_compose_file) up -d --build
	@echo "Restart complete."

clean:
	@echo "Cleaning volumes"
	docker system prune --volumes -f
	rm -rf docker/volumes/vol_mysql
