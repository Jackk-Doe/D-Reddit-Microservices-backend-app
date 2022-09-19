const TokenAuthServices = require("./tokenAuthServices");

class Utils {
    static async check_id_from_token_or_param_body(req) {
        /// Return token
        /// Return UserID
        /// Return None
        const token = req.headers.authorization.split(" ")[1];
        const decodedDatas = await TokenAuthServices.decodeToken(token);

        if (decodedDatas) {
            return decodedDatas.id;
        }

        const { id } = req.body;

        if (id) {
            return id
        }

        return null;
    }
}

module.exports = Utils;