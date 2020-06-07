FROM python:3
ENV PYTHONUNBUFFERED 1
RUN mkdir /code
COPY . /code/
RUN ls -la /code/
WORKDIR /code
RUN pip install -r requirements.txt
RUN python -m nltk.downloader stopwords
EXPOSE 8000
