FROM python:3.9

WORKDIR /app

COPY Pipfile* ./

RUN pip install pipenv

RUN pipenv install --system --deploy --ignore-pipfile

COPY movie_list ./movie_list
COPY migrations ./migrations


ENV FLASK_RUN_HOST 0.0.0.0

CMD flask db upgrade && flask movie_list deploy && flask run