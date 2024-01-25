FROM python:slim
COPY . /app
WORKDIR /app
RUN apt update && apt install -y cron chromium chromium-driver
RUN pip install -r requirements.txt
ENV DOCKER=1
CMD ["sh", "docker.sh"]