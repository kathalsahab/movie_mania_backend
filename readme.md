# RESTful MovieList

Python Flask backend application for Small MovieList RESTful APIs Project.

-   [MovieList](#MovieList)
-   [Run Project](#run-project)
    -   [Docker](#docker)
        -   [Makefile](#makefile)
        -   [Docker Compose](#docker-compose)
    -   [Flask locally](#flask-locally)
-   [Project Details](#project-details)
    -   [Directory Structure](#directory-structure)
    -   [Configurations](#configurations)
-   [Docker Commands Reference](#docker-commands-reference)
    -   [Docker - useful commands](#docker---useful-commands)
        -   [Build image](#build-image)
        -   [Run container in detached mode](#run-container-in-detached-mode)
        -   [Stop container](#stop-container)
        -   [Docker logs : -f to follow logs](#docker-logs---f-to-follow-logs)
        -   [Exec : run commands inside docker container](#exec--run-commands-inside-docker-container)
        -   [Docker cleanup commands](#docker-cleanup-commands)
        -   [Docker list all containers](#docker-list-all-containers)
    -   [Docker Compose - useful commands](#docker-compose---useful-commands)
        -   [Start containers](#start-containers)
        -   [Build the container and start docker compose in background](#build-the-container-and-start-docker-compose-in-background)
        -   [Shutdown the containers](#shutdown-the-containers)

# Run Project

> For testing refer postman collection present in ./movie_list/postman

## Docker

> Docker Install -> Refer https://docs.docker.com/engine/install/

> ⚠️ The Docker and compose files are development only and should **NOT** be used in production environment as it contains `flask run`.

### Makefile

The easiest way to run the MovieList application inside docker is to use `Makefile`

> `make` CLI utility is prerequisite. It is pre-configured in macOS.<br>Alternatively, use `docker-compose` commands described [below](#docker-compose).

```sh
make up
```

Stop the containers

```sh
make down
```

Stop and Re-run the containers

```sh
make restart
```

### Docker Compose

Alternatively, you can directly execute `docker-compose` commands that are written in Makefile.

> '`-f docker-compose.yml`' is optional if the compose file name exactly matches `docker-compose.yml`

Build and Run the Containers

```sh
docker-compose -f docker-compose.yml up -d --build
```

Stop the containers

```sh
docker-compose -f docker-compose.yml down
```

## Flask locally

To run the application locally you must have `.env` file in the `movie_list` folder.

> ⚠️ To run flask locally, please adjust the `SQLALCHEMY_DATABASE_URI` environment variable in `.env` file to point to local instance of mySQL.
>
> Alternatively, Just remove the `SQLALCHEMY_DATABASE_URI` variable from file. This will result in generation of local SQLite DB file `db.sqlite`

With current working directory as `movie_list` run -

```sh
flask run
```

# Project Details

## Directory Structure

All source code is in `movie_list` directory.

Code is modularized based on the Feature of the application. Each feature is grouped into its own directory following the undermentioned pattern.

```
feature_dir
├── models.py
└── v1
    ├── __init__.py
    ├── controllers.py
    └── routes.py
```

## Configurations

Development, Testing and Production configurations are separated in the `movie_list/config.py` file. All the required environment variables are extracted from OS in `movie_list/config.py` file and put into application config.

While development, required environment variables should be set in `.env` file which will be automatically loaded into the OS.

---

# Docker Commands Reference

-   Defined this app’s environment with a `Dockerfile` so it can be reproduced anywhere.
-   Define the services that make up this app in `docker-compose.yml` so they can be run together in an isolated environment.

## Docker - useful commands

### Build image

```sh
docker build -t movie_list .
```

### Run container in detached mode

```sh
docker run -it -d -p 5000:5000 movie_list
```

### Stop container

```sh
docker stop movie_list
```

### Docker logs : -f to follow logs

```sh
docker logs movie_list -f
```

### Exec : run commands inside docker container

`-i -t` : for making it interactive and tty session. This helps in exiting the container with <kbd>Cmd</kbd>+<kbd>c</kbd>

```sh
docker exec -it movie_list bash
```

### Docker cleanup commands

```sh
docker images prune
docker volume prune
docker system prune
```

### Docker list all containers

```sh
docker ps -a
```

## Docker Compose - useful commands

### Start containers

```sh
docker-compose up
```

### Build the container and start docker compose in background

```sh
docker-compose up -d --build
```

### Shutdown the containers

```sh
docker-compose down
```
