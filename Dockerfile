FROM  python:3.7
LABEL maintainer="wilson<wilsonlwx518@gmail.com>"
COPY . /app/
WORKDIR /app
ENV http_proxy http://10.239.4.160:913
ENV https_proxy http://10.239.4.160:913
RUN apt-get update
RUN mkdir -p /root/.pip \
    && mv ./pip.conf /root/.pip/ \
    && pip install -r requirements.txt


