FROM python:3.11.0-slim

RUN apt update
RUN apt install -y gcc

WORKDIR /usr/src/nawah

COPY . .

RUN python -m pip install -r requirements.txt
RUN python -m pip install .

CMD [ "nawah", "--version" ]
