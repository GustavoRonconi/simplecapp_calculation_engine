from calculation_engine.finops_commons import FinopsCommons
from calculation_engine.exceptions import InvalidPositionDayTrade
from calculation_engine.utils import SimpleCappUtils


class DayTradeCalculate(FinopsCommons):
    """To hander day_trade financial operation class"""

    def _calcule_day_trade_operation_monthly_params(
        self, operations: list, year_month: str, ticker: str, broker: str
    ) -> dict:
        """To calcule params of day_trade operations in a reference year_month, indexed by operation type and ticker"""
        monthly_params = {
            "position": 0,
            "average_purchase_price": None,
            "total_amount_purchase": 0,
            "total_amount_sale": 0,
            "total_units_purchase": 0,
            "total_units_sale": 0,
            "cgs": None,
            "irrf": 0,
        }

        for operation in operations:
            operation_month = operation.date.strftime("%m/%Y")
            if operation_month == year_month and operation.ticker == ticker and operation.broker == broker:
                monthly_params["total_amount_" + operation.operation_type] += operation.amount + (
                    operation.operation_costs * self.mapper_operation_type_factor[operation.operation_type]
                )
                monthly_params["total_units_" + operation.operation_type] += operation.units
                monthly_params["position"] += (
                    self.mapper_operation_type_factor[operation.operation_type] * operation.units
                )
                monthly_params["irrf"] += operation.irrf
        if monthly_params["position"] != 0:
            raise InvalidPositionDayTrade(f"Invalid position to ticker: {ticker}")

        monthly_params["result"] = (
            monthly_params["total_amount_sale"] - monthly_params["total_amount_purchase"]
        )

        return monthly_params

    def calcule_day_trade_operations(self, operations: list, **kwargs) -> list:
        tickers = SimpleCappUtils.get_unique_values(operations, "ticker")
        brokers = SimpleCappUtils.get_unique_values(operations, "broker")
        year_months_to_reference_year = self.compile_year_months_reference_year(operations[0].date.year)

        compile_day_trade_operations = {
            broker: {
                ticker: {
                    year_month: {
                        **{"year_month": year_month, "broker": broker, "ticker": ticker, "operation_class": "day_trade",},
                        **self._calcule_day_trade_operation_monthly_params(operations, year_month, ticker, broker),
                    }
                    for year_month in year_months_to_reference_year
                }
                for ticker in tickers
            }
            for broker in brokers
        }
        return SimpleCappUtils.unpack_dict_in_list_of_rows(3, compile_day_trade_operations)

    def process(self, operations) -> list:
        if not operations:
            return []
        agrouped_operations_by_ticker_type = self.agroup_operations_by_ticker_type(
            operations, self.mapper_ticker_types.keys()
        )

        sumamary_by_ticker = []
        for (ticker_type, operations,) in agrouped_operations_by_ticker_type.items():
            sumamary_by_ticker.extend(
                self.mapper_ticker_types[ticker_type].process(operations, self.calcule_day_trade_operations)
            )

        return sumamary_by_ticker
