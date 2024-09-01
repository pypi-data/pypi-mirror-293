FROM python:3.9-slim
WORKDIR /src
COPY ./cmd.py /src
COPY ./config.py.py /src
COPY ./config.yaml /src
RUN pip install AsyncURLCrawler
VOLUME /src/output
CMD ["python", "cmd.py", "--url", "https://pouyae.ir", "--exact", "--output", "/src/output"]
