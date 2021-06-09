from calculation_engine.utils import SimpleCappUtils
from calculation_engine.ticker_types import BDR, RealStateFunds, Stock


class FinopsCommons:
    """Commons operations to all financial operations"""

    mapper_ticker_types = {
        "fiis": RealStateFunds(),
        "stock": Stock(),
        "bdr": BDR(),
    }

    mapper_operation_type_factor = {"sale": -1, "purchase": 1}

    def agroup_operations_by_ticker_type(self, operations: list) -> dict:
        """To agroup financial operations by ticker type"""
        agrouped_operations_by_ticker_type = {
            ticker_type: SimpleCappUtils.get_list_with_filters({"ticker_type": ticker_type}, operations)
            for ticker_type in self.mapper_ticker_types.keys()
        }

        return agrouped_operations_by_ticker_type

    def compile_year_months_reference_year(self, reference_year: int) -> list:
        """To compile a list of years_months based in reference year"""
        return [f"{i:02d}/{reference_year}" for i in range(1, 13)]
