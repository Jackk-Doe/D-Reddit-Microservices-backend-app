const express = require('express');

const UserController = require('./controllers');

const router = express.Router();


/// For ADMIN uses  (or Testing)
router.get('/', UserController.getAll);
router.get('/:id', UserController.getUser);

/// Post-services mostly uses only these route(s)
router.post('/token', UserController.validateUserToken);
router.patch('/views/:id', UserController.updateView);

// TODO : a route to return User [views] 

/// For API-Gateway uses
router.post('/signup', UserController.signUp);
router.post('/signin', UserController.signIn);

module.exports = router;