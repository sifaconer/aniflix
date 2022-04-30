FROM mcr.microsoft.com/playwright:v1.21.0-focal
RUN apt update
WORKDIR /api

COPY ./api/.env /api/.env
COPY ./api/main.py /api/main.py
COPY ./api/play.py /api/play.py
COPY ./requirements.txt /api/requirements.txt

ENV FLASK_APP="/api/main.py"

RUN apt install -y python3-pip && pip install -r /api/requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"]
