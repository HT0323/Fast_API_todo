import jwt
from fastapi import HTTPException
from passlib.context import CryptContext
from datetime import datetime, timedelta
from decouple import config

JWT_KEY = config('JWT_KEY')


class AuthJwtCsrf():
    pwd_ctx = CryptContext(schemes=["bcrypt"], deprecated="auto")
    secret_key = JWT_KEY

    # ユーザーが入力したパスワードをハッシュ化
    def generate_hashed_pw(self, password) -> str:
        return self.pwd_ctx.hash(password)

    # ユーザーが入力したパスワードとハッシュ化したパスワードが一致するかをチェック

    def verify_pw(self, plain_pw, hashed_pw) -> bool:
        return self.pwd_ctx.verify(plain_pw, hashed_pw)

    # JWTトークンの生成

    def encode_jwt(self, email) -> str:
        payload = {
            'exp': datetime.utcnow() + timedelta(days=0, minutes=5),
            'iat': datetime.utcnow(),
            'sub': email
        }
        return jwt.encode(
            payload,
            self.secret_key,
            algorithm='HS256'
        )

    # JWTトークンの復号

    def decode_jwt(self, token) -> str:
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=['HS256'])
            return payload['sub']
        except jwt.ExpiredSignatureError:
            raise HTTPException(status_code=401, detail='The JWT has expired')
        except jwt.InvalidTokenError as e:
            raise HTTPException(status_code=401, detail='JWT is not valid')
