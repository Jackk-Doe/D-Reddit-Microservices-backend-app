## Thrid ver
FROM node:16-slim
#From now on the './' dir is pointed to './app'
WORKDIR /app

# install system dependencies
RUN apt-get update \
    && apt-get install gcc -y \
    && apt-get clean

COPY ./package*.json .
RUN npm install
COPY . .

ENV PORT=5000
# Either 'mongodb' or container name (user-services-db)
ENV CONNECTION_URL=mongodb://mongodb:27017/ 
ENV SECRET_KEY="THIS_IS_SUPPOSSED_TO_BE_A_SECRET_KEY_FOR_AUTH_FUNCTION"

EXPOSE 5000
CMD [ "node", "index.js" ]