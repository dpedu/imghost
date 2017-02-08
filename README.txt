IMGHOST

The simplest imghost

Install like:

pip3 install -r requirements.txt
python3 setup.py install
imghost

Then visit http://127.0.0.1:3000/

Dockerfile, based on http://gitlab.davepedu.com/dave/docker-nginx:

# docker build -t imghost -f docker/Dockerfile .
# docker run -it --rm -v /host/path:/usr/share/imghost/ui/i/ -p 8080:80 --name imghost imghost
