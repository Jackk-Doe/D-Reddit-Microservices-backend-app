FROM python:3.9

WORKDIR /app
COPY ./requirements.txt .
RUN pip install -r requirements.txt
COPY /app .

ENV PORT 3000
ENV POST_SERVICES_URL = "http://post-app:8000"
ENV USER_SERVICES_URL = "http://user-app:5000"

CMD [ "python", "app/main.py" ]