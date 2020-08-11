FROM python:3.8.0-slim
MAINTAINER saki.mohsen@gmail.com
# EXPOSE: PORT does not work on heroku
EXPOSE 8501
COPY requirements-app.txt usr/src/requirements.txt
COPY app usr/src/app
COPY models usr/src/models
WORKDIR /usr/src
RUN pip3 install -r requirements.txt
# $PORT is an environment variable provided by heroku
# Uncomment tail part of below command for heroku deployment 
CMD streamlit run app/app.py #--server.port $PORT
