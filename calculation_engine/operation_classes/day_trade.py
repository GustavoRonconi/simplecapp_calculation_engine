from calculation_engine import operation_classes
from calculation_engine.operation_classes.operation_classes_commons import OperationClassesCommons
from calculation_engine.exceptions import InvalidPositionDayTrade
from calculation_engine.utils import SimpleCappUtils


class DayTradeCalculate(OperationClassesCommons):
    """To hander day_trade financial operation class"""
    operation_class = "day_trade"

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
                    operation.operation_costs
                    * self.mapper_operation_type_factor[operation.operation_type.value]
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


    def _calcule_operations_by_ticker(self, operations: list, reference_year: int, year_months_to_reference_year: list, **kwargs):
        tickers = SimpleCappUtils.get_unique_values(operations, "ticker")
        brokers = SimpleCappUtils.get_unique_values(operations, "broker")

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
