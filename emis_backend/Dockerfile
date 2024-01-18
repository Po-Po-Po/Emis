FROM python:3.10.10-buster
ENV POSTGRES_DB=''
ENV POSTGRES_USER=''
ENV POSTGRES_PASSWORD=''
ENV POSTGRES_HOST=''


WORKDIR /
COPY requirements.txt ./
RUN apt -y update
RUN apt install -y\
    git \
    wget \
    curl \
    pkg-config \
    python3-dev \
    software-properties-common \
    && apt install -y locales && \
    sed -i -e 's/# ru_RU.UTF-8 UTF-8/ru_RU.UTF-8 UTF-8/' /etc/locale.gen && \
    dpkg-reconfigure --frontend=noninteractive locales \
    && apt clean && rm -rf /tmp/* /var/tmp/*

ENV LANG ru_RU.UTF-8
ENV LC_ALL ru_RU.UTF-8

RUN pip install --upgrade pip && pip install pyopenssl --upgrade && pip install --no-cache-dir -r requirements.txt
RUN rm requirements.txt

COPY . /app
WORKDIR /app
RUN python manage.py collectstatic --noinput
