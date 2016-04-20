FROM gliderlabs/alpine:3.3

WORKDIR /lytebot
COPY . /lytebot

RUN apk add --no-cache python3 python3-dev && \
    python3 -m ensurepip && \
    pip3 install --upgrade pip setuptools && \
    pip3 install -r requirements.txt && \
    python3 setup.py install

CMD lytebot
