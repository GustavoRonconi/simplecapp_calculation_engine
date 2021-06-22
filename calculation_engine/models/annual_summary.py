from typing import List, Optional

from pydantic import BaseModel

from calculation_engine.constants import OperationClassEnum, TickerTypeEnum
from calculation_engine.models.finantial_operation import FinantialOperation


class PreviewYearLoss(BaseModel):
    year_month: str
    ticker_type: TickerTypeEnum
    operation_class: OperationClassEnum
    accumulated_loss: float


class AnnualSummary(BaseModel):
    customer_name: str
    customer_cpf: str
    reference_year: int
    previous_year_loss: Optional[List[PreviewYearLoss]] = []
    financial_operations: List[FinantialOperation]
