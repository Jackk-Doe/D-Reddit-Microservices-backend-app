FROM python:3.9

WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir --upgrade -r requirements.txt
COPY . .

ENV DATABASE_URL "postgresql://root:password@postgres:5432/room-db"
ENV PORT 8000
ENV USER_SERVICES_URL "http://0.0.0.0:5000/users"

CMD [ "python", "app/main.py" ]