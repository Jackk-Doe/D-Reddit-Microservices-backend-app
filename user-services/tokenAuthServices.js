const jwt = require('jsonwebtoken');

class TokenAuthServices {

    /// Decode Datas from the [token]
    /// [decodedDatas] contains [email], [id] & [iat] fields
    static async decodeToken(token) {
        const decodedDatas = jwt.decode(token, process.env.SECRET_KEY);
        return decodedDatas;
    }
}

module.exports = TokenAuthServices;