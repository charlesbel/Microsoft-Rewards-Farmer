FROM python:3.9.2

RUN mkdir -p /rewards_bot/logs

RUN apt-get update
RUN apt-get install -y cron wget apt-transport-https

# install google chrome
RUN wget -q -O - https://dl-ssl.google.com/linux/linux_signing_key.pub | apt-key add -
RUN sh -c 'echo "deb [arch=amd64] http://dl.google.com/linux/chrome/deb/ stable main" >> /etc/apt/sources.list.d/google-chrome.list'
RUN apt-get -y update
RUN apt-get install -y google-chrome-stable

# install chromedriver
RUN apt-get install -yqq unzip
RUN wget -O /tmp/chromedriver.zip http://chromedriver.storage.googleapis.com/`curl -sS chromedriver.storage.googleapis.com/LATEST_RELEASE`/chromedriver_linux64.zip
RUN unzip /tmp/chromedriver.zip chromedriver -d /usr/local/bin/

# Set TZ
RUN apt-get install -y tzdata
ENV TZ=America/New_York

COPY . /data
WORKDIR /data
RUN pip install --no-cache-dir -r requirements.txt

# set display port to avoid crash
ENV DISPLAY=:99

# Custom Env Vars
ENV DOCKER_IMAGE=true

# Run the command on container startup
CMD ["python3", "-u", "/data/ms_rewards_farmer.py"]
