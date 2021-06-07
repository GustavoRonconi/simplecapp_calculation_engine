from typing import Callable

class BDR:
    """To handler BDR operations"""

    def process(self, operations: list, operation_function: Callable, average_price: dict = {},) -> dict:
        summary_by_ticker = []
        if len(operations) == 0:
            return summary_by_ticker

        summary_by_ticker.extend(operation_function(operations, **{"average_price": average_price}))

        return summary_by_ticker