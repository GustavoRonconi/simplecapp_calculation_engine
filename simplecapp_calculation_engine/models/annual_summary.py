from typing import List, Optional

from pydantic import BaseModel

from simplecapp_calculation_engine.constants import OperationClassEnum, TickerTypeEnum
from simplecapp_calculation_engine.models.finantial_operation import FinantialOperation


class PreviewYearLoss(BaseModel):
    year_month: str
    ticker_type: TickerTypeEnum
    operation_class: OperationClassEnum
    accumulated_loss: float


class AnnualSummary(BaseModel):
    profile_id: int
    reference_year: int
    previous_year_loss: Optional[List[PreviewYearLoss]] = []
    financial_operations: List[FinantialOperation]
