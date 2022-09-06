const mongoose = require('mongoose');

const UserSchema = mongoose.Schema({
    name: {
        type: String,
        required: true
    },
    email: {
        type: String,
        required: true
    },
    password: {
        type: String,
        required: true
    },
    role: {
        type: String,
        default: 'NORMAL'
    },
    bio: {
        type: String,
        required: true
    },
    // TODO : Add [views] dict field
    views: {
        type: Map,
        default: {}
    }
});

const UserModel = mongoose.model('user', UserSchema);

module.exports = UserModel;