const mongoose = require('mongoose');

/// Create a database connection
async function mongodbConnection(url) {
    try {
        await mongoose.connect(url);
        console.log("Successfully connected to database");
    } catch (error) {
        console.log(error);
        process.exit();
    }
}

module.exports = mongodbConnection;