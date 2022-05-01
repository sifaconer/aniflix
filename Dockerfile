FROM mcr.microsoft.com/playwright:v1.21.0-focal
RUN apt update
WORKDIR /app

COPY ./.env /app/.env
COPY ./api/__init__.py /app/api/__init__.py
COPY ./api/main.py /app/api/main.py
COPY ./api/play.py /app/api/play.py
COPY ./wsgi.py /app/wsgi.py
COPY ./requirements.txt /app/requirements.txt

ENV FLASK_APP="/app/wsgi.py"

RUN apt install -y python3-pip && pip install -r /app/requirements.txt

CMD ["flask", "run", "--host", "0.0.0.0"]
