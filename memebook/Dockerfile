FROM python:3.7-alpine
RUN apk add --no-cache build-base linux-headers git

WORKDIR /usr/src/app

COPY app/requirements.txt app/memebook.py ./
COPY app/templates/main.html ./templates/main.html

RUN pip install --no-cache-dir -r requirements.txt
RUN pip install git+https://github.com/DataDog/dd-trace-py.git@master#egg=ddtrace

CMD [ "python", "./memebook.py" ]
