FROM python:3.8.6-buster

WORKDIR /usr/src/r_app

COPY . /usr/src/r_app/

RUN pip install -r ./requirements.txt

CMD ["uwsgi", "app.ini"]
