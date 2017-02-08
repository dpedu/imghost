FROM dpedu/nginx

RUN apt-get update ; \
    apt-get install -y supervisor python3-pip python3-setuptools

ADD . /usr/share/imghost/

RUN cd /usr/share/imghost ;\
    pip3 install -r requirements.txt ;\
    python3 setup.py install ;\
    rm -rf scenv README.txt  build  dist  docker  imghost  imghost.egg-info  requirements.txt  setup.py ui/i/* .git ; \
    chown www-data /usr/share/imghost/ui/i

ADD docker/supervisor-imghost.conf /etc/supervisor/conf.d/imghost.conf
ADD docker/default /etc/nginx/sites-enabled/default

# WORKDIR /usr/share/imghost
