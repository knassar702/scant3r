FROM python:3.8
WORKDIR /home/scant3r
RUN apt update -y && apt upgrade -y
RUN apt install python3 -y
RUN apt install python3-dev -y
RUN apt install python3-pip -y
RUN pip3 install requests fake-useragent 
RUN pip3 install requests_toolbelt flask
COPY . /home/scant3r/
ENTRYPOINT ["python3","scant3r.py"]
