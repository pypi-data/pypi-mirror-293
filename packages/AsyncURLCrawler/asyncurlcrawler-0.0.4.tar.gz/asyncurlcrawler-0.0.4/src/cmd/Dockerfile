FROM python:3.9-slim
WORKDIR /src
COPY . /src
RUN pip install httpx==0.25.2
RUN pip install beautifulsoup4==4.12.2
RUN pip install pyyaml==6.0.1
RUN pip install tldextract==5.1.1
RUN pip install AsyncURLCrawler
VOLUME /src/output
CMD ["python", "cmd.py", "--url", "https://pouyae.ir", "--exact", "--output", "/src/output"]
