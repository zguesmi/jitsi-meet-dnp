# FROM python:3.8-slim-buster
FROM python:alpine3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install requirements
RUN apk add bash
RUN python -m pip install docker

# ENV CONFIG ~/.jitsi-meet-cfg
# RUN bash -c "mkdir -p ${CONFIG}/{web/letsencrypt,transcripts,prosody/config,prosody/prosody-plugins-custom,jicofo,jvb,jigasi,jibri}"
# RUN echo $CONFIG

COPY main.py /app/main.py
COPY jitsi.py /app/jitsi.py

EXPOSE ${HTTP_PORT} ${HTTPS_PORT}
CMD ["python", "/app/main.py"]
