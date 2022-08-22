const express = require('express');

const UserController = require('./controllers');

const router = express.Router();

router.get('/test', async (req, res) => res.json({ message: 'Testing API Route!' }));

/// FOR TESTING ONLY
router.get('/', UserController.getAll);

router.get('/:id', UserController.getUser);

router.post('/signup', UserController.signUp);
router.post('/signin', UserController.signIn);

module.exports = router;