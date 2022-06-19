FROM python:3.10-slim
WORKDIR /scant3r
COPY . .
RUN pip install --no-cache-dir .
ENTRYPOINT ["scant3r"]
CMD ["-h"]
