FROM 226817515299.dkr.ecr.eu-west-1.amazonaws.com/python:2

USER root
COPY . .
RUN set -ex && pip install -r requirements.dev.txt
USER $DEF_USER:$DEF_USER
