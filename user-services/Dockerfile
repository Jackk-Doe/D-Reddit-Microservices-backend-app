## Thrid ver
FROM node:16
WORKDIR /app  #From now on the './' dir is point to './app'
COPY package*.json ./
RUN npm install
COPY . .
# ENV PORT=5000
# ENV CONNECTION_URL=mongodb://localhost:27017/mongodb
EXPOSE 5000
CMD [ "node", "index.js" ]