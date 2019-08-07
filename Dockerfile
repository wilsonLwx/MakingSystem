FROM  python:3.7
LABEL maintainer="wilson<wilsonlwx518@gmail.com>"
COPY . /app/
WORKDIR /app
RUN mkdir -p /root/.pip \
    && mv ./pip.conf /root/.pip/ \
    && pip install -r requirements.txt

