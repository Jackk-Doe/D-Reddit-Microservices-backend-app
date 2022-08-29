const express = require('express');

const UserController = require('./controllers');

const router = express.Router();


/// For ADMIN uses  (or Testing)
router.get('/', UserController.getAll);
router.get('/:id', UserController.getUser);

/// Post-services mostly uses only these route(s)
router.post('/token', UserController.validateUserToken);

// TODO : a route to update (+) [views] in models.js
// TODO : a route to return User [views] 

/// For API-Gateway uses
router.post('/signup', UserController.signUp);
router.post('/signin', UserController.signIn);

module.exports = router;