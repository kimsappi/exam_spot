FROM python:3.7.5-alpine

LABEL maintainer="Jordane GENGO (Titus) <jordane@hive.fi>"
LABEL version="0.0.1"

RUN apk add tzdata build-base postgresql-dev libffi-dev openssl-dev

RUN pip3 install --upgrade pip
COPY requirements.txt /
RUN pip3 install -r requirements.txt

COPY . /app
WORKDIR /app

CMD ["/app/entrypoint.sh"]
