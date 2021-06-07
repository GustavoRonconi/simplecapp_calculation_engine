import calendar
from datetime import date

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

    def _get_unique_year_months(self, operations: list) -> list:
        """To get a unique year months"""
        year_months = []
        for operation in operations:
            year_month = str(operation.date.year) + str(operation.date.month)
            if year_month not in year_months:
                year_months.append(year_month)

        return year_months

    def agroup_operations_by_ticker_type(self, operations: list, ticker_types: list) -> dict:
        """To agroup financial operations by ticker type"""
        agrouped_operations_by_ticker_type = {
            ticker_type: SimpleCappUtils.get_list_with_filters({"ticker_type": ticker_type}, operations)
            for ticker_type in ticker_types
        }

        return agrouped_operations_by_ticker_type

    def compile_year_months_reference_year(self, reference_year: int) -> list:
        """To compile a list of years months based in reference year"""
        return [f"{i:02d}/{reference_year}" for i in range(1, 13)]

    def _get_last_position_average_price_for_month(
        self, average_price_by_ticker: dict, year_month: str
    ) -> dict:
        """To get a last position and average price for a specific month"""
        month, year = year_month.split("/")
        max_date = date(int(year), int(month), calendar.monthrange(int(year), int(month))[1])
        average_price_reference = (
            next(iter(average_price_by_ticker)),
            average_price_by_ticker[next(iter(average_price_by_ticker))],
        )
        for reference_date, average_price in average_price_by_ticker.items():
            if reference_date <= max_date:
                average_price_reference = reference_date, average_price

        if average_price_reference[0] <= max_date:
            average_price_reference[1].pop("total_amount_with_operation_costs", None)
            average_price_reference[1].pop("operation_type", None)
            return average_price_reference[1]

        return {"position": 0.0, "average_purchase_price": 0.0}
