FROM python:3.9-alpine

# RUN sed -i 's/dl-cdn.alpinelinux.org/mirrors.aliyun.com/g' /etc/apk/repositories

WORKDIR /app

COPY ./requirements.txt /app/requirements.txt

RUN apk add --update --no-cache --virtual .tmp gcc libc-dev linux-headers && \
    apk add --no-cache jpeg-dev zlib-dev && \
    pip install -r /app/requirements.txt && \
    apk del .tmp && rm /app/requirements.txt

COPY ./captcha_app /app/captcha_app
COPY ./run.py /app/run.py

EXPOSE 5000
CMD ["python", "run.py"]

