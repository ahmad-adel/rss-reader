FROM python:3.11.4

# Install required packages and remove the apt packages cache when done.
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --fix-missing \
    nano \
    build-essential \
    git \
    wget \
    curl \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-setuptools \
    python3-pip \
    python3-numpy \
    software-properties-common \
    zip \
    nginx \
    supervisor \
    redis-server && \
    pip3 install uwsgi

COPY supervisor-app.conf /etc/supervisor/conf.d/

COPY requirements.txt /home/ubuntu/code/app/

RUN pip3 install -r /home/ubuntu/code/app/requirements.txt

COPY . /home/ubuntu/code/

RUN chmod 777 -R /home/ubuntu/code/
RUN mkdir -p /home/ubuntu/logs

COPY nginx-configs/default /etc/nginx/sites-available/default

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 80

ENV DJANGO_SETTINGS_MODULE='rss_reader.settings'
ENV CELERYD_CHDIR='/home/ubuntu/code/app'

CMD ["supervisord", "-n"]

