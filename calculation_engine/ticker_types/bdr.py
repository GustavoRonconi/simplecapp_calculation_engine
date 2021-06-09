from typing import Callable


class BDR:
    """To handler BDR operations"""

    def process(
        self, operations: list, reference_year: int, operation_function: Callable, average_price: dict = {},
    ) -> dict:
        output_by_ticker_type = {"summary_by_ticker": [], "custody_by_ticker_and_reference_year": []}
        if len(operations) == 0:
            return output_by_ticker_type

        return operation_function(operations, reference_year, **{"average_price": average_price})

