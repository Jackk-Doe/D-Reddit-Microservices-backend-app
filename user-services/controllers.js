const UserModel = require('./models');

class UserController {
    static async getUser(req, res) {
        UserModel.findById(req.params.id)
            .then(user => res.status(200).json(user))
            .catch(error => res.status(404).json({ error: 'User not found'}));
    }

    static async signIn(req, res) {}

    static async signUp(req, res) {}
}

module.exports = UserController;