FROM tiangolo/meinheld-gunicorn:python3.7

LABEL maintainer="João Marcos <joaomarccos.ads@gmail.com>"

ARG mongo_uri=mongodb://localhost:27017/weeding

ARG app_secret=SECRET

ENV MONGO_URI=$mongo_uri

ENV APP_SECRET=$app_secret

COPY ./app/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app
