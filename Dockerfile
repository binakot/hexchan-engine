FROM nikolaik/python-nodejs:python3.7-nodejs10

ENV FAKE_CONTENT=false

RUN mkdir /app
WORKDIR /app
EXPOSE 8000

RUN apt-get update && \
    apt-get install -y postgresql-client

COPY requirements.txt /app/
RUN pip install --upgrade pip && \
    pip install -r requirements.txt

COPY package*.json /app/
RUN npm install

COPY . .
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python3"]
