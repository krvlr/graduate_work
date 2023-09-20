FROM python:3.10
WORKDIR /opt/app
COPY requirements.txt .
RUN pip install --upgrade pip && pip install -r requirements.txt --no-cache-dir
RUN python -m nltk.downloader punkt && python -m nltk.downloader wordnet && python -m nltk.downloader stopwords
COPY src .
ENTRYPOINT ["gunicorn", "main:app", "--bind", "0.0.0.0:8000", "-k", "uvicorn.workers.UvicornWorker"]