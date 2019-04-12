FROM nikolaik/python-nodejs:python3.7-nodejs10

RUN mkdir /app
WORKDIR /app
EXPOSE 8000

COPY requirements.txt /app/
RUN pip install -r requirements.txt

COPY package*.json /app/
RUN npm install

COPY . .
RUN chmod +x /app/docker-entrypoint.sh

ENTRYPOINT ["/app/docker-entrypoint.sh"]
CMD ["python3"]
