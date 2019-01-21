FROM python:3.7-alpine

COPY requirements.txt requirements.txt
RUN apk update && \
    apk add postgresql && \
    rm -rf /var/cache/apk/*

RUN pip install -r requirements.txt

COPY . /app
WORKDIR /app

# for the flask config
ENV FLASK_ENV=prod

EXPOSE 5000
ENTRYPOINT [ "gunicorn", "-b", "0.0.0.0:5000", "--log-level", "INFO", "manage:app" ]
