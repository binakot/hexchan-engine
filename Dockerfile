FROM tiangolo/uwsgi-nginx:python3.7-alpine3.9

WORKDIR /app

RUN apk add --no-cache \
        bash \
        build-base python3-dev musl-dev postgresql-dev zlib-dev jpeg-dev freetype-dev \
        nodejs nodejs-npm \
        postgresql-client

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY package*.json /app/
RUN npm install

COPY . .
RUN chmod +x /app/prestart.sh
