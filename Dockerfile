FROM python:3.6
ENV PYTHONUNBUFFERED 1

ENV MAGINE_HOME=/magine

RUN mkdir $MAGINE_HOME
WORKDIR $MAGINE_HOME
ADD requirements.txt requirements-production.txt $MAGINE_HOME/
RUN pip install -r requirements-production.txt
ADD . $MAGINE_HOME
CMD ["uwsgi"]
