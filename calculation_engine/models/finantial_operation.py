from datetime import date
from typing import List, Optional

from pydantic import BaseModel, root_validator


class FinantialOperation(BaseModel):
    date: date
    operation_type: str
    operation_class: str
    ticker: str
    ticker_type: str
    units: float
    unitary_value: float
    amount: Optional[float] = None
    emoluments: Optional[float] = None
    currency_code: str

    @root_validator
    def amount_none(cls, values):
        if not (values["amount"]):
            values["amount"] = values["units"] * values["unitary_value"]
        return values

    @root_validator
    def emoluments_none(cls, values):
        if not (values["emoluments"]):
            values["emoluments"] = 0
        return values

