FROM gliderlabs/alpine:3.3

WORKDIR /lytebot
COPY . /lytebot

RUN apk add --no-cache python3 openssl ca-certificates
RUN apk add --no-cache --virtual build-dependencies wget \
    && wget "https://bootstrap.pypa.io/get-pip.py" -O /dev/stdout | python3 \
    && pip3 install -r requirements.txt \
    && python3 setup.py install \
    && apk del build-dependencies

CMD lytebot
