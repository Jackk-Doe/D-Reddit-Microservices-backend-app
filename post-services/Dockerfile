FROM python:3.9-slim

WORKDIR /usr/src/app

# install system dependencies
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV DATABASE_URL "postgresql://root:password@postgres:5432/room-db"
ENV PORT 8000
ENV USER_SERVICES_URL "http://user-app:5000/users"
ENV CONTENT_RECOMMEND_SERVICES_URL "http://content-recommend-app:8080"

CMD [ "python", "app/main.py" ]