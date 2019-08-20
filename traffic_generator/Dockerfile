FROM python:3.7-alpine
RUN apk add --no-cache build-base linux-headers

WORKDIR /usr/src/app

COPY app/requirements.txt app/traffic_generator.py ./
COPY app/templates/main.html ./templates/main.html

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "python", "./traffic_generator.py" ]
