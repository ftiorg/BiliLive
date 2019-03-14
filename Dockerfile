FROM continuumio/miniconda3:latest

WORKDIR /app

ADD docker/condarc /root/.condarc
ADD docker/sources.list /etc/apt/sources.list
ADD docker/pip.conf /root/.pip/pip.conf
ADD . /app

RUN conda install -y opencv pillow numpy

CMD ['entrypoint.sh']

ENTRYPOINT ['/bin/sh']
