# pull official base image
FROM python:3.10-slim-buster

# set working directory
WORKDIR /usr/src

# set environment variables
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# install system dependencies
RUN apt-get update \
  && apt-get -y --no-install-recommends install netcat gcc postgresql \
  && apt-get clean

# install python dependencies
RUN pip install --no-cache-dir --upgrade pip
COPY ./requirements/*.txt ./requirements/
RUN pip install --no-cache-dir -r ./requirements/dev.txt

# run fastapi project
COPY ./compose/local/start /start
RUN sed -i 's/\r$//g' /start \
  && chmod +x /start

# add app
COPY . .

# add entrypoint.sh
COPY entrypoint.sh .
RUN chmod +x /usr/src/entrypoint.sh

# run entrypoint.sh
ENTRYPOINT ["/usr/src/entrypoint.sh"]
