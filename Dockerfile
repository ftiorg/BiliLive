FROM continuumio/miniconda3:latest
LABEL maintainer="kamino <kamino@imea.me>"
WORKDIR /app

ADD docker/condarc /root/.condarc
ADD docker/sources.list /etc/apt/sources.list
ADD docker/pip.conf /root/.pip/pip.conf
ADD . /app

RUN conda install -y opencv pillow numpy mutagen

CMD ["entrypoint.sh"]

ENTRYPOINT ["sh"]
