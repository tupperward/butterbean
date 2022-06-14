
FROM alpine:3.15

RUN apk update \
  && apk add --no-cache \
            bash \
            postgresql12-client \
            python3 py-pip \
  && pip install python-magic

COPY application/ /data/
COPY /etc/butterbean/ /tmp/
WORKDIR /data

CMD ["./entrypoint.sh"]