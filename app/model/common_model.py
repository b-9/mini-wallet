from pydantic import BaseModel, validator
from uuid import UUID


class Token(BaseModel):
    authorization: str

    @validator("authorization")
    def token_validator(cls, value):
        if value[:6] == "Token ":
            value = value[6:]
        else:
            raise ValueError("not valid token format")

        try:
            value = str(UUID(value))
        except Exception as e:
            raise ValueError("not valid token format")

        return value
