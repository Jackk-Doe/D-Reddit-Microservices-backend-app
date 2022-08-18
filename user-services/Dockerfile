## Thrid ver
FROM node:16
#From now on the './' dir is pointed to './app'
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
ENV PORT=5000
# Either 'mongodb' or container name (user-services-db)
ENV CONNECTION_URL=mongodb://mongodb:27017/ 
EXPOSE 5000
CMD [ "node", "index.js" ]