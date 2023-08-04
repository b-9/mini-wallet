from pydantic import BaseModel


class WithDrawals(BaseModel):
    amount: float
    reference_id: str


class Deposits(BaseModel):
    amount: float
    reference_id: str


class DisableWallet(BaseModel):
    is_disabled: bool
