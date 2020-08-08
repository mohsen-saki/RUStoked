FROM python:3.8
MAINTAINER saki.mohsen@gmail.com
EXPOSE 8501
COPY requirements-app.txt usr/src/requirements.txt
COPY app usr/src/app
COPY models usr/src/models
WORKDIR /usr/src
RUN pip3 install -r requirements.txt
CMD streamlit run app/app.py
