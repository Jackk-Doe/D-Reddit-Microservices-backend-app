FROM python:3.9

WORKDIR /app
COPY ./requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .

ENV PORT 8080

CMD [ "python", "app/main.py" ]