FROM python:3.6-alpine
COPY . /app
WORKDIR /app
RUN apk add --update curl gcc g++ \
    && rm -rf /var/cache/apk/*

RUN ln -s /usr/include/locale.h /usr/include/xlocale.h

RUN pip install -r requirements.txt
CMD ["gunicorn", "-w 4", "main:app"]