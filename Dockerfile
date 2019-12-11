FROM tiangolo/meinheld-gunicorn:python3.7

LABEL maintainer="João Marcos <joaomarccos.ads@gmail.com>"

COPY ./app/requirements.txt requirements.txt

RUN pip install -r requirements.txt

COPY ./app /app
