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

// For testing api route
app.get('/', async (req, res) => res.json({ message: 'Testing User API Route!' }));

mongodbConnection(CONNECTION_URL);

app.listen(PORT, () => {
    console.log(`Server running on PORT : ${PORT}`);
});