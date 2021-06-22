from enum import Enum


class OperationTypeEnum(str, Enum):
    purchase = "purchase"
    sale = "sale"


class OperationClassEnum(str, Enum):
    day_trade = "day_trade"
    normal = "normal"


class TickerTypeEnum(str, Enum):
    stock = "stock"
    bdr = "bdr"
    fiis = "fiis"
