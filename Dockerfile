FROM python:3.11

WORKDIR /backend

RUN apt-get update && apt-get install -y libgl1 libglib2.0-0
COPY requirements.txt requirements.txt

RUN pip install -r requirements.txt


COPY backend /backend

# RUN adduser --disabled-password service-user
# USER service-user

EXPOSE 8000
