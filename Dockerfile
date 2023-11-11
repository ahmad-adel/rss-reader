FROM python:3.11.4

# Install required packages and remove the apt packages cache when done.
RUN apt-get update && \
    apt-get upgrade -y && \
    apt-get install -y --fix-missing \
    nano \
    build-essential \
    cmake \
    gfortran \
    git \
    wget \
    curl \
    graphicsmagick \
    libgraphicsmagick1-dev \
    libavcodec-dev \
    libavformat-dev \
    libgtk2.0-dev \
    libjpeg-dev \
    liblapack-dev \
    libswscale-dev \
    pkg-config \
    python3-dev \
    python3-setuptools \
    python3-pip \
    python3-numpy \
    software-properties-common \
    zip \
    supervisor \
    redis-server \
    poppler-utils && \
    pip3 install -U pip setuptools && \
    pip3 install uwsgi

#REDIS Configs
RUN echo "vm.overcommit_memory = 1" > /etc/sysctl.conf

COPY supervisor-app.conf /etc/supervisor/conf.d/

COPY requirements.txt /home/ubuntu/code/app/

RUN pip3 install -r /home/ubuntu/code/app/requirements.txt

COPY . /home/ubuntu/code/

RUN chmod 777 -R /home/ubuntu/code/
RUN mkdir -p /home/ubuntu/logs

ENV LC_ALL=C.UTF-8
ENV LANG=C.UTF-8

EXPOSE 8080

ENV DJANGO_SETTINGS_MODULE='rss_reader.settings'
ENV CELERYD_CHDIR='/home/ubuntu/code/app'

CMD ["supervisord", "-n"]

