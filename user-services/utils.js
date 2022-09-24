const TokenAuthServices = require("./tokenAuthServices");

class Utils {

    /// Return UserID : generates from Header-Auth-Token or Request-body
    static async check_id_from_token_or_param_body(req) {

        /// Via Auth-Token : update User.views
        if (req.headers.authorization) {
            console.log("FOUND HEADER AUTH Token, with Request");
            const token = req.headers.authorization.split(" ")[1];
            const decodedDatas = await TokenAuthServices.decodeToken(token);
    
            if (decodedDatas) {
                return decodedDatas.id;
            }
        }

        /// Via UserID : update User.views
        if (req.body.id) {
            const { id } = req.body;
            return id;
        }

        return null;
    }
}

module.exports = Utils;