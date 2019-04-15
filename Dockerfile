FROM continuumio/miniconda3:latest
LABEL maintainer="kamino <kamino@imea.me>"
WORKDIR /app

ENV TZ 'Asia/Shanghai'

ADD docker/condarc /root/.condarc
ADD docker/sources.list /etc/apt/sources.list
ADD docker/pip.conf /root/.pip/pip.conf
ADD docker/nginx.conf /usr/local/nginx/conf/nginx.conf
ADD . /app

RUN conda install -y opencv ffmpeg pillow numpy mutagen flask pymysql aiohttp requests &&\
    apt update &&\
    apt install -y git build-essential libssl-dev procps &&\
    cd /usr/src &&\
    apt source nginx &&\
    git clone https://github.com/arut/nginx-rtmp-module.git &&\
    cd nginx-1* &&\
    ./configure \
        --add-module=../nginx-rtmp-module \
        --without-select_module \
        --without-poll_module \
        --without-http_charset_module \
        --without-http_gzip_module \
        --without-http_ssi_module \
        --without-http_userid_module \
        --without-http_access_module \
        --without-http_auth_basic_module \
        --without-http_mirror_module \
        --without-http_autoindex_module \
        --without-http_geo_module \
        --without-http_map_module \
        --without-http_split_clients_module \
        --without-http_referer_module \
        --without-http_rewrite_module \
        --without-http_proxy_module \
        --without-http_fastcgi_module \
        --without-http_uwsgi_module \
        --without-http_scgi_module \
        --without-http_grpc_module \
        --without-http_memcached_module \
        --without-http_limit_conn_module \
        --without-http_limit_req_module \
        --without-http_empty_gif_module \
        --without-http_browser_module \
        --without-http_upstream_hash_module \
        --without-http_upstream_ip_hash_module \
        --without-http_upstream_least_conn_module \
        --without-http_upstream_keepalive_module \
        --without-http_upstream_zone_module \
        --without-http-cache \
        --without-mail_pop3_module \
        --without-mail_imap_module \
        --without-mail_smtp_module \
        --without-stream_limit_conn_module \
        --without-stream_access_module \
        --without-stream_geo_module \
        --without-stream_map_module \
        --without-stream_split_clients_module \
        --without-stream_return_module \
        --without-stream_upstream_hash_module \
        --without-stream_upstream_least_conn_module \
        --without-stream_upstream_zone_module \
        --without-pcre &&\
    make &&\
    make install &&\
    make clean &&\
    rm /usr/src/* -rf &&\
    apt autoremove -y git build-essential libssl-dev &&\
    conda clean --tarballs -y

CMD ["entrypoint.sh"]

ENTRYPOINT ["sh"]
