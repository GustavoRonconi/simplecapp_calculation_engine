from typing import List

from calculation_engine.models.finantial_operation import FinantialOperation
from pydantic import BaseModel

from calculation_engine.constants import TickerTypeEnum, OperationClassEnum


class PreviewYearResult(BaseModel):
    year_month: str
    ticker_type: TickerTypeEnum
    operation_class: OperationClassEnum
    result: float


class AnnualSummary(BaseModel):
    customer_name: str
    customer_cpf: str
    reference_year: int
    previous_year_results: List[PreviewYearResult]
    financial_operations: List[FinantialOperation]
