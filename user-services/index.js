const express = require('express');
const dotenv = require('dotenv');
const cors = require('cors');

const router = require('./routes');
const mongodbConnection = require('./database');


const app = express();

// .env 
dotenv.config();
const PORT = process.env.PORT || 5000;
const CONNECTION_URL = process.env.CONNECTION_URL;

// Loaders
app.use(cors());
app.use(express.json());
app.use('/users', router);


await mongodbConnection(CONNECTION_URL);

app.listen(PORT, () => {
    console.log(`Server running on PORT : ${PORT}`);
});