FROM python:3.7-alpine

RUN apk add --no-cache build-base linux-headers

WORKDIR /usr/src/app
COPY app/requirements.txt app/doggo.py ./

RUN pip install --no-cache-dir -r requirements.txt

CMD [ "ddtrace-run", "python", "doggo.py" ]
