FROM python:3.6.9

WORKDIR /home/scant3r
RUN apt update -y && apt upgrade -y
RUN useradd -d /home/scant3r/ -m -p scant3r -s /bin/bash scant3r
RUN echo "scant3r:scant3r" | chpasswd # change your password after up you docker container echo "scant3r:bruh41414" | chpasswd
RUN apt install python3 -y
RUN apt install python3-dev -y
RUN apt install python3-pip -y
RUN apt install sudo -y
RUN apt install uwsgi -y
RUN python3 -m pip install Flask-Limiter uwsgi requests flask
RUN apt install uwsgi-plugin-python -y
COPY . /home/scant3r/
RUN rm Dockerfile
RUN chown -R scant3r:scant3r /home/ctf
USER scant3r
EXPOSE 6030
ENTRYPOINT ["uwsgi","--http","0.0.0.0:6030","app.ini","--plugin","python3"]
