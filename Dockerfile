FROM continuumio/miniconda3:latest
LABEL maintainer="kamino <kamino@imea.me>"
WORKDIR /app

ENV TZ 'Asia/Shanghai'

ADD docker/sources.list /etc/apt/sources.list
ADD docker/pip.conf /root/.pip/pip.conf
ADD docker/nginx.conf /usr/local/nginx/conf/nginx.conf
ADD . /app

RUN conda install -y opencv ffmpeg pillow numpy mutagen flask pymysql aiohttp requests pycrypto &&\
    apt update &&\
    apt install -y git build-essential libssl-dev procps &&\
    apt autoremove -y git build-essential libssl-dev &&\
    conda clean --tarballs -y

CMD ["entrypoint.sh"]

ENTRYPOINT ["sh"]
