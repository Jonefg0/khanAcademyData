FROM python:3.6.7-slim

# Version: 1.4
# Dockerfile to build the coroner container.

# Install Python and Package Libraries
RUN apt-get update && apt-get upgrade -y && apt-get autoremove && apt-get autoclean
RUN apt-get install -y \
    libffi-dev \
    libssl-dev \
    default-libmysqlclient-dev \
    libxml2-dev \
    libxslt-dev \
    libjpeg-dev \
    libfreetype6-dev \
    zlib1g-dev \
    net-tools \
    nano

ARG PROJECT=khandata
ARG PROJECT_DIR=/var/www/${PROJECT}
WORKDIR $PROJECT_DIR

ENV PYTHONUNBUFFERED 1

RUN mkdir -p $PROJECT_DIR
COPY . .

RUN pip install --upgrade pip
RUN pip install -r $PROJECT_DIR/requirements.txt

EXPOSE 8000
STOPSIGNAL SIGINT
ENTRYPOINT ["python", "manage.py"]
CMD ["runserver", "0.0.0.0:8000"]
