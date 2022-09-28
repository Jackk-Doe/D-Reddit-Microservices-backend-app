const express = require('express');

const UserController = require('./controllers');

const router = express.Router();


/// For ADMIN uses  (or Testing)
router.get('/account', UserController.getAll);
router.get('/account/:id', UserController.getUser);

/// Post-services mostly uses only these route(s)
router.get('/views', UserController.getUserViews);
router.patch('/views', UserController.updateView);
router.post('/token', UserController.validateUserToken);

/// For API-Gateway uses   (DIRECT uses)
router.post('/signup', UserController.signUp);
router.post('/signin', UserController.signIn);

module.exports = router;