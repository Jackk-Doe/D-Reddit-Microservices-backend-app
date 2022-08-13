const express = require('express');
const dotenv = require('dotenv');

const router = require('./routes');
const mongodbConnection = require('./database');


const app = express();

dotenv.config();

app.use(express.json());
app.use('/users', router);

const PORT = process.env.PORT || 5000;
const CONNECTION_URL = process.env.CONNECTION_URL;

await mongodbConnection(CONNECTION_URL);

app.listen(PORT, () => {
    console.log(`Server running on PORT : ${PORT}`);
});