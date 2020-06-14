FROM python:alpine3.8

# Keeps Python from generating .pyc files in the container
ENV PYTHONDONTWRITEBYTECODE 1
# Turns off buffering for easier container logging
ENV PYTHONUNBUFFERED 1

# Install requirements
RUN apk add bash
RUN python -m pip install docker

COPY main.py /app/main.py
COPY env.py /app/env.py

CMD ["python", "/app/main.py"]
