FROM python:3.6

RUN apt-get update
RUN apt-get install -y

ENV MY_HOME "/opt/app"
WORKDIR $MY_HOME

COPY ./ /opt/app/

RUN ls -lra /opt/app/

RUN pip3 install -r /opt/app/requirements.txt

CMD ["python", "/opt/app/consumer-retry.py"]