FROM python:3-alpine

COPY requirements.txt /

RUN apk --update add tzdata git \
  && cp /usr/share/zoneinfo/Etc/UTC /etc/localtime \
  && pip install -r /requirements.txt \
  && apk del git \
  && rm -fR /root/.cache

WORKDIR /tmp/x
COPY laporte_journal/*py ./laporte_journal/
COPY setup.py README.md MANIFEST.in LICENSE requirements.txt ./
RUN  pip install . 

ENTRYPOINT [ "laporte-journal" ]
