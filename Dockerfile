FROM python:3.6
ENV PYTHONUNBUFFERED 1

ENV MAGINE_HOME=/magine_home

RUN mkdir $MAGINE_HOME
WORKDIR $MAGINE_HOME
ADD requirements.txt requirements-production.txt $MAGINE_HOME/
ADD . $MAGINE_HOME
RUN pip install -r requirements-production.txt
ENV PYTHONPATH /magine_home/Magine:$PYTHONPATH
CMD ["uwsgi"]
