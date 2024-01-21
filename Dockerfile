FROM tiangolo/uwsgi-nginx:python3.11

WORKDIR /app

RUN apt-get update && \
    apt-get install -y --no-install-recommends \
        bash \
        build-essential \
        python3-dev \
        libpq-dev \
        zlib1g-dev \
        libjpeg-dev \
        libfreetype6-dev \
        nodejs \
        npm \
        postgresql-client && \
    rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY package*.json /app/
RUN npm install

COPY . .
RUN chmod +x /app/prestart.sh