FROM vernacularai/ubuntu-pyenv:2.0.0


ARG PYTHON_VER=3.8.6
ARG POETRY_VER=1.0.10
ARG VERSION

WORKDIR /home/slu

RUN apt-get update && apt-get install -y gcc g++ && \
    pyenv install $PYTHON_VER && pyenv global $PYTHON_VER && \
    pip install --upgrade pip && \
    pip install poetry==$POETRY_VER

RUN poetry config virtualenvs.create false

COPY pyproject.toml poetry.lock /home/slu/

RUN poetry install --no-dev && \ 
    rm -rf /root/.cache && pip3 uninstall --yes poetry

COPY ./slu ./slu
COPY ./data/${VERSION}/models ./data/${VERSION}/models
COPY ./uwsgi ./uwsgi
COPY ./config ./config

ENV GOOGLE_API_KEY="" \
    DUCKLING_URL="" \
    ENVIRONMENT="PRODUCTION" \
    GOOGLE_API_KEY="" \
    SENTRY_DSN=""

EXPOSE 8005

CMD ["/bin/sh", "-ec", "while :; do echo '.'; sleep 5 ; done"]
