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
                monthly_params["total_amount_" + operation.operation_type.value] += operation.amount + (
                    operation.operation_costs * self.mapper_operation_type_factor[operation.operation_type.value]
                )
                monthly_params["total_units_" + operation.operation_type.value] += operation.units
                monthly_params["position"] += (
                    self.mapper_operation_type_factor[operation.operation_type.value] * operation.units
                )
                monthly_params["irrf"] += operation.irrf
        if monthly_params["position"] != 0:
            raise InvalidPositionDayTrade(f"Invalid position to ticker: {ticker}")

        monthly_params["result"] = (
            monthly_params["total_amount_sale"] - monthly_params["total_amount_purchase"]
        )

        return monthly_params

    def calcule_day_trade_operations(self, operations: list, reference_year: int, **kwargs) -> dict:
        tickers = SimpleCappUtils.get_unique_values(operations, "ticker")
        brokers = SimpleCappUtils.get_unique_values(operations, "broker")
        year_months_to_reference_year = self.compile_year_months_reference_year(reference_year)

        summary_by_ticker = {
            broker: {
                ticker: {
                    year_month: {
                        **{
                            "year_month": year_month,
                            "broker": broker,
                            "ticker": ticker,
                            "operation_class": "day_trade",
                        },
                        **self._calcule_day_trade_operation_monthly_params(
                            operations, year_month, ticker, broker
                        ),
                    }
                    for year_month in year_months_to_reference_year
                }
                for ticker in tickers
            }
            for broker in brokers
        }
        return {
            "summary_by_ticker": SimpleCappUtils.unpack_dict_in_list_of_rows(3, summary_by_ticker),
            "custody_by_ticker_and_reference_year": [],
        }

    def process(self, operations: list, reference_year: int) -> dict:
        if not operations:
            return {"summary_by_ticker": [], "custody_by_ticker_and_reference_year": []}
        agrouped_operations_by_ticker_type = self.agroup_operations_by_ticker_type(operations)

        output_by_operation_class = {"summary_by_ticker": [], "custody_by_ticker_and_reference_year": []}
        for (ticker_type, operations,) in agrouped_operations_by_ticker_type.items():
            output_by_ticker_type = self.mapper_ticker_types[ticker_type].process(
                operations, reference_year, self.calcule_day_trade_operations
            )
            output_by_operation_class["summary_by_ticker"].extend(output_by_ticker_type["summary_by_ticker"])
            output_by_operation_class["custody_by_ticker_and_reference_year"].extend(
                output_by_ticker_type["custody_by_ticker_and_reference_year"]
            )

        return output_by_operation_class
