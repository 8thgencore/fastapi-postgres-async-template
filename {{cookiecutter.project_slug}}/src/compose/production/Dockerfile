# -----------------------------------------------------------------------------
# Base stage
# -----------------------------------------------------------------------------
# pull official base image
FROM python:3.11-slim-buster AS base

# install system dependencies
RUN apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y --no-install-recommends curl git build-essential netcat gcc postgresql \
  && apt-get autoremove -y

# install poetry using the official script 
ENV POETRY_HOME="/opt/poetry"
RUN curl -sSL https://install.python-poetry.org | python3 -

# -----------------------------------------------------------------------------
# Install stage
# -----------------------------------------------------------------------------
FROM base AS install

# set working directory
WORKDIR /usr/src

# allow controlling the poetry installation of dependencies via external args
ARG INSTALL_ARGS="--no-root --no-dev"
ENV POETRY_HOME="/opt/poetry"
ENV PATH="$POETRY_HOME/bin:$PATH"
COPY pyproject.toml poetry.lock ./

# install without virtualenv, since we are inside a container
RUN poetry config virtualenvs.create false \
  && poetry install $INSTALL_ARGS

# cleanup
RUN curl -sSL https://install.python-poetry.org | python3 - --uninstall
RUN apt-get purge -y curl git build-essential gcc \
  && apt-get clean -y \
  && rm -rf /root/.cache \
  && rm -rf /var/apt/lists/* \
  && rm -rf /var/cache/apt/*

# -----------------------------------------------------------------------------
# App-image stage
# -----------------------------------------------------------------------------
FROM install as app-image

# run fastapi project
COPY ./compose/local/start /start
RUN sed -i 's/\r$//g' /start \
  && chmod +x /start

# add app
COPY . .

# add entrypoint.sh
COPY entrypoint.sh .
RUN chmod +x /usr/src/entrypoint.sh

# add new user
RUN addgroup --system fastapi \
  && adduser --system --ingroup fastapi fastapi

# select custom user
RUN chown -R fastapi:fastapi /usr/src

USER fastapi

# run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]
