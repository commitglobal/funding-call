help:                             ## Display a help message detailing commands and their purpose
	@echo "Commands:"
	@grep -E '^([a-zA-Z_-]+:.*?## .*|#+ (.*))$$' $(MAKEFILE_LIST) | awk 'BEGIN {FS = ":.*?## "}; {printf "\033[36m%-30s\033[0m %s\n", $$1, $$2}'
	@echo ""


## [Managing the project]
### Stopping the containers and dropping the databases
stop-sqlite:                      ## stops the sqlite dev project
	docker compose down -t 60

drop-sqlite:                      ## stops the sqlite dev project
	docker compose down -v -t 60
	rm -rf ./backend/.db_sqlite

stop-mysql:                       ## stops the mysql dev project
	docker compose -f docker-compose.mysql.yml down -t 60

drop-mysql:                       ## stops the mysql dev project
	docker compose -f docker-compose.mysql.yml down -v -t 60

stop-psql:                       ## stops the psql dev project
	docker compose -f docker-compose.psql.yml down -t 60

drop-psql:                       ## stops the psql dev project
	docker compose -f docker-compose.psql.yml down -v -t 60

stop-prod:                        ## stops the mysql dev project
	docker compose -f docker-compose.prod.yml down -t 60

drop-prod:                        ## stops the mysql dev project
	docker compose -f docker-compose.prod.yml down -v -t 60

### Building & starting the containers
up-sqlite:                        ## run the project with sqlite
	docker compose up --build

upd-sqlite:                       ## run the project with sqlite in detached mode
	docker compose up -d --build

up-mysql:                         ## run the project with mysql
	docker compose -f docker-compose.mysql.yml up --build

upd-mysql:                        ## run the project with mysql in detached mode
	docker compose -f docker-compose.mysql.yml up -d --build

up-psql:                         ## run the project with psql
	docker compose -f docker-compose.psql.yml up --build

upd-psql:                        ## run the project with psql in detached mode
	docker compose -f docker-compose.psql.yml up -d --build

up-prod:                         ## run the project with mysql
	docker compose -f docker-compose.prod.yml up --build

upd-prod:                        ## run the project with mysql in detached mode
	docker compose -f docker-compose.prod.yml up -d --build

### Using the SQLite database
run-sqlite: stop-psql stop-mysql up-sqlite   ## run the project with sqlite and stop the mysql project beforehand
rund-sqlite: stop-psql stop-mysql upd-sqlite ## run the project with sqlite in detached mode and stop the mysql project beforehand
redo-sqlite: drop-sqlite up-sqlite           ## delete the db and rerun the project with sqlite
redod-sqlite: drop-sqlite upd-sqlite         ## delete the db and rerun the project with sqlite in detached mode

### Using the MySQL database
run-mysql: stop-psql stop-sqlite up-mysql    ## run the project with mysql and stop the sqlite project beforehand
rund-mysql: stop-psql stop-sqlite upd-mysql  ## run the project with mysql in detached mode and stop the sqlite project beforehand
redo-mysql: drop-mysql up-mysql              ## delete the db and rerun the project with mysql
redod-mysql: drop-mysql upd-mysql            ## delete the db and rerun the project with mysql in detached mode

### Using the PostgreSQL database
run-psql: stop-mysql stop-sqlite up-psql      ## run the project with psql and stop the mysql project beforehand
rund-psql: stop-mysql stop-sqlite upd-psql    ## run the project with psql in detached mode and stop the mysql project beforehand
redo-psql: drop-psql up-psql                  ## delete the db and rerun the project with psql
redod-psql: drop-psql upd-psql                ## delete the db and rerun the project with psql in detached mode

### With an image built for production
run-prod: up-prod                 ## run the project with production settings
rund-prod: upd-prod               ## run the project with production settings in detached mode
redo-prod: drop-prod up-prod      ## delete the db and rerun the project with mysql
redod-prod: drop-prod upd-prod    ## delete the db and rerun the project with mysql in detached mode

### Other run options
run: run-sqlite                   ## set the default run command to sqlite
redo: redo-sqlite                 ## set the default redo command to sqlite
rund: rund-sqlite                 ## set the default run command to sqlite
redod: redod-sqlite               ## set the default redo command to sqlite

stop: stop-sqlite stop-mysql stop-psql stop-prod ## stop all running projects

drop: drop-sqlite drop-mysql drop-psql drop-prod ## drop all databases


## [Monitoring the containers]
logs-dev:                         ## show the logs of the containers
	docker logs -f funding_call_dev

logs: logs-dev                    ## set the default logs command to dev

logs-prod:                        ## show the logs of the containers
	docker logs -f funding_call_prod


## [Django operations]
makemigrations:                   ## generate migrations in a clean container
	docker exec funding_call_dev sh -c "python3 -Wd ./backend/manage.py makemigrations $(apps)"

migrate:                          ## apply migrations in a clean container
	docker exec funding_call_dev sh -c "python3 -Wd ./backend/manage.py migrate $(apps)"

migrations: makemigrations migrate ## generate and apply migrations

makemessages:                     ## generate the strings marked for translation
	docker exec funding_call_dev sh -c "python3 -Wd ./backend/manage.py makemessages -a"

compilemessages:                  ## compile the translations
	docker exec funding_call_dev sh -c "python3 -Wd ./backend/manage.py compilemessages"

messages: makemessages compilemessages ## generate and compile the translations

collectstatic:                    ## collect the static files
	docker exec funding_call_dev sh -c "python3 -Wd ./backend/manage.py collectstatic --no-input"

format:                           ## format the code with ruff
	docker exec funding_call_dev sh -c " \
		cd ./backend && \
		ruff format . &&  \
		ruff check --select I --fix ."

check:
	docker exec funding_call_dev sh -c " \
		cd ./backend && \
		ruff check --select I . && \
		ruff format --check ."

pyshell:                          ## start a django shell
	docker exec -it funding_call_dev sh -c "python3 -Wd ./backend/manage.py shell"

sh:                               ## start a sh shell
	docker exec -it funding_call_dev sh -c "sh"

bash:                             ## start a bash shell
	docker exec -it funding_call_dev sh -c "bash"


## [Requirements management]
requirements-build:               ## run pip compile and add requirements from the *.in files
	docker exec funding_call_dev sh -c " \
		cd ./backend && \
		uv sync --active \
	"

requirements-update:              ## run pip compile and rebuild the requirements files
	docker exec funding_call_dev sh -c " \
		cd ./backend && \
		uv sync --active -U \
	"


## [Tests]
tests:                            ## run the tests
	docker exec funding_call_dev sh -c "cd ./backend && pytest -Wd $(apps)"

tests-cover:                      ## run the tests with coverage
	docker exec funding_call_dev sh -c "cd ./backend && pytest -Wd  --cov --cov-report=xml --cov-report=term-missing --cov-fail-under=60 $(apps)"


## [Clean-up]
clean-docker:                     ## stop docker containers and remove orphaned images and volumes
	docker compose -f docker-compose.mysql.yml down -t 60
	docker compose -f docker-compose.psql.yml down -t 60
	docker compose down -t 60
	docker compose -f docker-compose.prod.yml down -t 60
	docker system prune -f

clean-extras:                        ## remove test, coverage, file artifacts, and compiled message files
	find ./backend -name '*.mo' -delete
	find ./backend -name '*.pyc' -delete
	find ./backend -name '*.pyo' -delete
	find ./backend -name '.coverage' -delete
	find ./backend -name '.pytest_cache' -delete
	find ./backend -name '.ruff_cache' -delete
	find ./backend -name '__pycache__' -delete
	find ./backend -name 'htmlcov' -delete

clean-db:                          ## remove the database files
	rm -rf ./backend/media ./backend/static ./frontend/dist

clean: clean-docker clean-extras clean-db  ## remove all build, test, coverage and Python artifacts

