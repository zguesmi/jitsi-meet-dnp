# FROM python:3.8-slim-buster
FROM python:alpine3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install pip requirements
RUN python -m pip install docker

RUN mkdir -p ~/.jitsi-meet-cfg/{web/letsencrypt,transcripts,prosody/config,prosody/prosody-plugins-custom,jicofo,jvb,jigasi,jibri}

COPY start.py /start.py

EXPOSE 80 443
CMD ["python", "/start.py"]
