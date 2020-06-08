FROM alpine:3

COPY ./locust/ /locust/
RUN apk --no-cache -U add python3-dev alpine-sdk linux-headers && \
    if [ ! -e /usr/bin/python ]; then ln -sf python3 /usr/bin/python ; fi && \
    \
    echo "**** install pip ****" && \
    python3 -m ensurepip && \
    rm -r /usr/lib/python*/ensurepip && \
    pip3 install --no-cache --upgrade pip setuptools wheel && \
    if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
    pip install pyzmq --install-option="--zmq=bundled" && \
    pip install locustio==0.14.6 && \
    pip install Faker && \
    chmod +x ./locust/start-locust.sh

WORKDIR /locust
EXPOSE 8089 5557 5558

ENTRYPOINT ["./start-locust.sh"]