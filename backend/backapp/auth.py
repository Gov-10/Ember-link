from .models import EmberUser
from ninja.security import HttpBearer
from jose import jwk, jwt
from jose.utils import base64url_decode
from datetime import datetime
import requests
from dotenv import load_dotenv
load_dotenv()
import os
COGNITO_REGION=os.getenv("COGNITO_REGION")
USER_POOL_ID = os.getenv("USER_POOL_ID")
USER_POOL_CLIENT_ID = os.getenv("USER_POOL_CLIENT_ID")
JWKS_URL = f"https://cognito-idp.{COGNITO_REGION}.amazonaws.com/{USER_POOL_ID}/.well-known/jwks.json"
JWKS = requests.get(JWKS_URL).json()["keys"]

def validate_token(token:str):
    headers = jwt.get_unverified_headers(token)
    kid = headers["kid"]
    jwt_key = next((key for key in JWKS if key["kid"] == kid), None)
    if not jwt_key:
        raise Exception("Public key not found")
    claims = jwt.get_unverified_claims(token)
    if claims["exp"] < datetime.utcnow().timestamp():
        raise Exception("Token expired")
    aud = claims.get("aud") or claims.get("client_id")
    if aud != USER_POOL_CLIENT_ID:
        raise Exception("Invalid audience")
    message, encoded_sig = token.rsplit(".", 1)
    decoded_sig = base64url_decode(encoded_sig.encode())
    public_key = jwk.construct(jwt_key)
    if not public_key.verify(message.encode(), decoded_sig):
        raise Exception("Invalid signature")
    return claims

class CustomAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            claims = validate_token(token)
            sub = claims["sub"]
            phone = claims.get("phone_number", "")
            groups= claims.get("cognito:groups", [])
            role= "ngo" if "ngos" in groups else "user"
            user, _ = EmberUser.objects.get_or_create(
            cognito_sub=sub,
            defaults={"phone": phone, "role": role}
        )
            return user
        except Exception as e:
            print("Auth error:", e)
            return None

