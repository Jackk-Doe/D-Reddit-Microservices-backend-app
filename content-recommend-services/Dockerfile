FROM python:3.9-slim

WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PORT 8080

CMD [ "python", "app/main.py" ]