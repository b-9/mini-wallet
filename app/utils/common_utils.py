from app.model.common_model import Token
from fastapi.exceptions import HTTPException


async def get_token(authorization):
    try:
        token_object = Token(authorization=authorization)
    except ValueError as ve:
        raise HTTPException(400, detail={"error": "Not a valid token format"})
    token = token_object.authorization
    return token
