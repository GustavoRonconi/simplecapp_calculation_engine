from typing import Callable


class TickerTypesCommons:
    """Commons operations to all ticker types"""

    def get_ir_flag(self, total_amount_sale: float) -> bool:
        return total_amount_sale > self.exception_sale_limit or self.exception_sale_limit == 0

    def calcule_ir_to_pay(self, result: float, accumulated_loss: float, irrf: float) -> float:
        result_with_accumulated_loss = result - abs(accumulated_loss)
        if result_with_accumulated_loss <= 0:
            return 0
        return (result_with_accumulated_loss * self.index_ir) - irrf

    def process(
        self,
        operations: list,
        reference_year: int,
        previous_year_loss: list,
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
            operations, reference_year, previous_year_loss, **{"average_price": average_price}
        )
