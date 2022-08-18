const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

const UserModel = require("./models");

class UserController {
  static async getUser(req, res) {
    UserModel.findById(req.params.id)
      .then((user) => res.status(200).json(user))
      .catch((error) => res.status(404).json({ error: "User not found" }));
  }

  static async signUp(req, res) {
    const { name, email, password, role, bio } = req.body;
    try {
      // Check if User already existed
      const existedAccount = await UserModel.findOne({ email });
      if (existedAccount) {
        return res
          .status(400)
          .json({ detail: "User with email already existed" });
      }

      // Generated password with Salt lvl of 12
      const hashedPassword = await bcrypt.hash(password, 12);

      // Create new User
      const user = await UserModel.create({
        name,
        email,
        password: hashedPassword,
        role,
        bio,
      });

      // Generate JWT token
      const token = jwt.sign(
        { email: user.email, id: user._id },
        process.env.SECRET_KEY
      );

      res.status(201).json({ user, token });

    } catch (error) {
      res.status(500).json({ detail: "Can't create account", error });
    }
  }

  static async signIn(req, res) {}
}

module.exports = UserController;
