from typing import Callable


class TickerTypesCommons:
    """Commons operations to all ticker types"""

    def get_ir_flag(self, total_amount_sale: float) -> bool:
        return total_amount_sale > self.exception_sale_limit or self.exception_sale_limit == 0

    def calcule_ir_to_pay(self, result: float, previous_loss: float, irrf: float) -> float:
        result_with_previous_loss = result - abs(previous_loss)
        if result_with_previous_loss <= 0:
            return 0
        return (result_with_previous_loss * self.index_ir) - irrf

    def process(
        self,
        operations: list,
        reference_year: int,
        previous_year_results: list,
        operation_function: Callable,
        average_price: dict = {},
    ) -> dict:
        output_by_ticker_type = {
            "summary_by_ticker": [],
            "custody_by_ticker_and_reference_year": [],
            "summary_by_monthly": [],
        }
        if len(operations) == 0:
            return output_by_ticker_type

        return operation_function(
            operations, reference_year, previous_year_results, **{"average_price": average_price}
        )
