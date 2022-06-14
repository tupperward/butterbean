
FROM alpine:latest

RUN apk update \
  && apk add --no-cache \
            bash \
            postgresql13-client \
            python3 py-pip \
  && pip install python-magic

COPY application/ /data/
COPY db/*.sql /tmp/
WORKDIR /data
RUN chown $(whoami) /data/*
RUN chmod +x /data/*
CMD ["./entrypoint.sh"]