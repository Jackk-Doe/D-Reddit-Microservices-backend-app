const bcrypt = require("bcryptjs");
const jwt = require("jsonwebtoken");

const UserModel = require("./models");
const TokenAuthServices = require("./tokenAuthServices");
const Utils = require("./utils");

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
      // If a given [id] field is not in 24 hex character, it throws error (mongoose)
      const existedUser = await UserModel.findById(req.params.id);

      if (!existedUser) {
        //! Error : User not existed
        return res.status(404).json({ detail: "User not found" });
      }

      const userRead = {
        name: existedUser.name,
        id: existedUser._id,
        email: existedUser.email,
        role: existedUser.role,
        bio: existedUser.bio,
      };

      res.status(200).json({ user: userRead });
    } catch (error) {
      res.status(500).json({ detail: "Error, can not get User" });
    }
  }

  /// POST [ /users/token ]
  static async validateUserToken(req, res) {
    try {
      // Get TOKEN
      const token = req.headers.authorization.split(" ")[1];

      const { id: _user_id } = await TokenAuthServices.decodeToken(token);

      const existedUser = await UserModel.findById(_user_id);
      if (!existedUser) {
        //! Error : User not existed
        return res.status(404).json({ detail: "User not found" });
      }

      res.status(200).json({ user_id: _user_id });
    } catch (error) {
      res.status(500).json({ detail: "Error, problem with token decoding", error})
    }
  }

  /// PATCH [ /views ]
  static async updateView(req, res) {
    try {

      /// Update User.views via either : Auth-Token || UserID in Req-Body
      const userId = await Utils.check_id_from_token_or_param_body(req);

      const existedUser = await UserModel.findById(userId);
      if (!existedUser) {
        return res.status(404).json({ detail: "User not found" });
      }

      // Get a List[int] of topics ID in body
      const { topics_id } = req.body;

      topics_id.forEach((_topic_id) => {
        const _topic_id_str = _topic_id.toString();
        
        // If no [_topic_id] in User's [views],  set views[_topic_id] to 0
        let _current_view = existedUser.views.get(_topic_id_str);
        if (!_current_view) {
          _current_view = 0;
        }

        // Update views count
        const _update_view_count = _current_view + 1;
        existedUser.views.set(_topic_id_str, _update_view_count);
      });
      
      const updatedUser = await UserModel.findByIdAndUpdate(userId, existedUser, { new: true });

      res.status(200).json({ user: updatedUser });

    } catch (error) {
      console.log(error);
      res.status(500).json({ detail: "Update VIEW failed", error})
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

      /// Create JWT token,
      /// from User's email + User's ID
      const token = jwt.sign(
        { email: user.email, id: user._id },
        process.env.SECRET_KEY
      );

      // TODO : in [user] must not include password and ID
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
        //! Error : Wrong password
        return res.status(404).json({ detail: "Wrong password" });
      }

      /// Receive JWT token,
      /// from User's email + User's ID
      const token = jwt.sign(
        { email: user.email, id: user._id },
        process.env.SECRET_KEY
      );

      // TODO : in [user] must not include password and ID
      res.status(200).json({ user, token });
    } catch (error) {
      res.status(500).json({ detail: "Can't login an account", error });
    }
  }
}

module.exports = UserController;
