from datetime import date
from enum import Enum

from typing import Optional

from pydantic import BaseModel, root_validator


class OperationTypeEnum(str, Enum):
    purchase = "purchase"
    sale = "sale"


class OperationClassEnum(str, Enum):
    day_trade = "day_trade"
    normal = "normal"


class TickerType(str, Enum):
    stock = "stock"
    bdr = "bdr"
    fiis = "fiis"


class FinantialOperation(BaseModel):
    date: date
    operation_type: OperationTypeEnum
    operation_class: OperationClassEnum
    ticker: str
    ticker_type: TickerType
    units: float
    unitary_value: float
    amount: Optional[float] = None
    operation_costs: Optional[float] = None
    irrf: Optional[float] = None
    currency_code: str

    @root_validator
    def to_set_none_values(cls, values):
        if not (values["amount"]):
            values["amount"] = values["units"] * values["unitary_value"]
        if not (values["operation_costs"]):
            values["operation_costs"] = 0
        if not (values["irrf"]):
            values["irrf"] = 0
        return values
