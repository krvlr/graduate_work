FROM python:3.10-alpine3.18
WORKDIR /opt/app
COPY . .
RUN pip install -r requirements.txt
RUN crontab crontab
CMD ["crond", "-f"]