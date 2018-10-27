# http://www.eidel.io/2017/07/10/dockerizing-django-uwsgi-postgres/

FROM python:3.6

RUN apt-get update
RUN apt-get install -y
RUN pip3 install uwsgi

ENV MY_HOME "/opt/app"
WORKDIR $MY_HOME

COPY ./ /opt/app/

RUN ls -lra /opt/app/

RUN pip3 install -r /opt/app/requirements.txt

ENV DJANGO_ENV=prod
ENV DOCKER_CONTAINER=1

EXPOSE 8000

CMD ["uwsgi", "--ini", "/opt/app/uwsgi.ini"]