const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

const UserModel = require("./models");

class UserController {

  static async getAll(req, res) {
    try {
      const users = await UserModel.find();
      res.status(200).json({ users: users });
    } catch (error) {
      res.status(500).json({ detail: "Can't get users"})
    }
  }

  static async getUser(req, res) {
    try {
      const user = await UserModel.findById(req.params.id);

      if (!user) {
        return res.status(404).json({ detail: "User not found" });
      }

      const userRead = {
        name: user.name,
        id: user._id,
        email: user.email,
        role: user.role,
        bio: user.bio,
      };

      res.status(200).json({ user: userRead });
    } catch (error) {
      res.status(500).json({ detail: "Can't get User" });
    }
  }

  /// POST [ /users/signup ]
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
      res.status(500).json({ detail: "Can't create account" });
    }
  }

  /// POST [ /users/signin ]
  static async signIn(req, res) {
    const { email, password } = req.body;
    try {
      const user = await UserModel.findOne({ email });
      // Check if User existed
      if (!user) {
        return res.status(404).json({ detail: "User not found" });
      }

      // Check User inputed password
      const isPasswordCorrect = await bcrypt.compare(password, user.password);
      if (!isPasswordCorrect) {
        return res.status(404).json({ detail: "Wrong password" });
      }

      // Generate JWT token
      const token = jwt.sign(
        { email: user.email, id: user._id },
        process.env.SECRET_KEY
      );

      res.status(200).json({ user, token });
    } catch (error) {
      res.status(500).json({ detail: "Can't login an account", error });
    }
  }
}

module.exports = UserController;
