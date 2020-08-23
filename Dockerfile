LABEL description="ScanT3r - Web Security Scanner"
FROM python:3.8
WORKDIR /home/scant3r
RUN apt update -y && apt upgrade -y
