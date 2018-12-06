FROM python:3.6
ENV PYTHONUNBUFFERED 1

ENV MAGINE_HOME=/magine_home

RUN mkdir $MAGINE_HOME
WORKDIR $MAGINE_HOME
RUN git clone https://github.com/LoLab-VU/MAGINE Magine

ADD . $MAGINE_HOME
RUN pip install -r requirements-production.txt
ENV PYTHONPATH /magine_home/Magine:$PYTHONPATH
