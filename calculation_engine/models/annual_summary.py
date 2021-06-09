from typing import List

from calculation_engine.models.finantial_operation import FinantialOperation
from pydantic import BaseModel


class AnnualSummary(BaseModel):
    customer_name: str
    customer_cpf: str
    reference_year: int
    financial_operations: List[FinantialOperation]
