FROM python:alpine3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install requirements
RUN apk add bash
RUN python -m pip install docker pyfiglet

COPY jitsi.py utils.py /app/

CMD ["python", "/app/jitsi.py"]
