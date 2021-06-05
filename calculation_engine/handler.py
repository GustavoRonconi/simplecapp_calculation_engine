import json
import calendar
from datetime import date
from typing import Callable

from calculation_engine.exceptions import InvalidAnnualSummary
from calculation_engine.models.annual_summary import AnnualSummary
from calculation_engine.utils import SimpleCappUtils
from calculation_engine.exceptions import InvalidPositionDayTrade


class RealStateFunds:
    """To handler real state funds operations"""

    def process(
        self, operations: list, operation_function: Callable, average_price: dict = {},
    ) -> dict:
        summary_by_ticker = []
        summary_by_ticker = []
        if len(operations) == 0:
            return summary_by_ticker

        summary_by_ticker.extend(
            operation_function(operations, **{"average_price": average_price})
        )

        return summary_by_ticker


class Stock:
    """To handler stook operations"""

    def process(
        self, operations: list, operation_function: Callable, average_price: dict = {},
    ) -> dict:
        summary_by_ticker = []
        summary_by_ticker = []
        if len(operations) == 0:
            return summary_by_ticker

        summary_by_ticker.extend(
            operation_function(operations, **{"average_price": average_price})
        )

        return summary_by_ticker


class BDR:
    """To handler BDR operations"""

    def process(
        self, operations: list, operation_function: Callable, average_price: dict = {},
    ) -> dict:
        summary_by_ticker = []
        if len(operations) == 0:
            return summary_by_ticker

        summary_by_ticker.extend(
            operation_function(operations, **{"average_price": average_price})
        )

        return summary_by_ticker


class FinopsCommons:
    """Commons operations to all financial operations"""

    mapper_ticker_types = {
        "fiis": RealStateFunds(),
        "stook": Stock(),
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

    def agroup_operations_by_ticker_type(
        self, operations: list, ticker_types: list
    ) -> dict:
        """To agroup financial operations by ticker type"""
        agrouped_operations_by_ticker_type = {
            ticker_type: SimpleCappUtils.get_list_with_filters(
                {"ticker_type": ticker_type}, operations
            )
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
        max_date = date(
            int(year), int(month), calendar.monthrange(int(year), int(month))[1]
        )
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


class DayTradeCalculate(FinopsCommons):
    """To hander day-trade financial operation class"""

    def _calcule_day_trade_operation_monthly_params(
        self, operations: list, year_month: str, ticker: str,
    ) -> dict:
        """To calcule params of day-trade operations in a reference year_month, indexed by operation type and ticker"""
        monthly_params = {
            "position": 0,
            "average_purchase_price": None,
            "total_amount_purchase": 0,
            "total_amount_sale": 0,
            "total_units_purchase": 0,
            "total_units_sale": 0,
            "cgs": None,
        }

        for operation in operations:
            operation_month = operation.date.strftime("%m/%Y")
            if operation_month == year_month and operation.ticker == ticker:
                monthly_params["total_amount_" + operation.operation_type] += (
                    operation.amount
                    + (
                        operation.operation_costs
                        * self.mapper_operation_type_factor[operation.operation_type]
                    )
                )
                monthly_params[
                    "total_units_" + operation.operation_type
                ] += operation.units
                monthly_params["position"] += (
                    self.mapper_operation_type_factor[operation.operation_type]
                    * operation.units
                )
        if monthly_params["position"] != 0:
            raise InvalidPositionDayTrade(f"Invalid position to ticker: {ticker}")

        monthly_params["result"] = (
            monthly_params["total_amount_sale"]
            - monthly_params["total_amount_purchase"]
        )

        return monthly_params

    def calcule_day_trade_operations(self, operations: list, **kwargs) -> list:
        tickers = SimpleCappUtils.get_unique_values(operations, "ticker")
        year_months_to_reference_year = self.compile_year_months_reference_year(
            operations[0].date.year
        )

        compile_day_trade_operations = {
            ticker: {
                year_month: {
                    **self._calcule_day_trade_operation_monthly_params(
                        operations, year_month, ticker
                    ),
                    **{
                        "year_month": year_month,
                        "ticker": ticker,
                        "operation_class": "day-trade",
                    },
                }
                for year_month in year_months_to_reference_year
            }
            for ticker in tickers
        }
        return SimpleCappUtils.unpack_dict_in_list_of_rows(
            2, compile_day_trade_operations
        )

    def process(self, operations) -> list:
        agrouped_operations_by_ticker_type = self.agroup_operations_by_ticker_type(
            operations, self.mapper_ticker_types.keys()
        )

        sumamary_by_ticker = []
        for (ticker_type, operations,) in agrouped_operations_by_ticker_type.items():
            sumamary_by_ticker.extend(
                self.mapper_ticker_types[ticker_type].process(
                    operations, self.calcule_day_trade_operations
                )
            )

        return sumamary_by_ticker


class NormalCalculate(FinopsCommons):
    """To hander normal financial operation class"""

    def _calcule_average_purchase_price_certain_day(
        self, day: date, operations_by_ticker: list, average_price_ticket: dict,
    ):

        """To calculate average price up to a certain day"""
        mapper_math_operations_by_operation_type = {
            "sale": lambda x, y, z=0: x - (y - z),
            "purchase": lambda x, y, z=0: x + (y + z),
        }

        amount_to_calc_average_price = 0
        position_to_calc_average_price = 0

        for operation in operations_by_ticker:
            if operation.date <= day:

                # TO APPLY POSITION
                average_price_ticket[operation.ticker][day][
                    "position"
                ] = mapper_math_operations_by_operation_type[operation.operation_type](
                    average_price_ticket[operation.ticker][day]["position"],
                    operation.units,
                )

                # CONDITION AVERAGE PRICE
                if operation.operation_type == "purchase":
                    amount_to_calc_average_price = mapper_math_operations_by_operation_type[
                        operation.operation_type
                    ](
                        amount_to_calc_average_price,
                        operation.amount,
                        operation.operation_costs,
                    )
                    position_to_calc_average_price = mapper_math_operations_by_operation_type[
                        operation.operation_type
                    ](
                        position_to_calc_average_price, operation.units
                    )

            if operation.date == day:
                average_price_ticket[operation.ticker][day][
                    "operation_type"
                ] = operation.operation_type
                if position_to_calc_average_price <= 0:
                    average_price_ticket[operation.ticker][day][
                        "average_purchase_price"
                    ] = None
                    continue
                average_price_ticket[operation.ticker][day][
                    "average_purchase_price"
                ] = (amount_to_calc_average_price / position_to_calc_average_price)

        return average_price_ticket

    def _calcule_average_purchase_price_for_each_sale(self, operations: list) -> dict:
        """To calcule average purchase price for each sale operation"""

        ordered_operations = sorted(operations, key=lambda x: x.date)

        asset_portfolio = SimpleCappUtils.get_unique_values(
            ordered_operations, "ticker"
        )

        operations_by_ticker = SimpleCappUtils.index_list_by_list_of_keys(
            ordered_operations, asset_portfolio, "ticker"
        )

        operations_days_by_ticker = {
            ticker: sorted(list(set([operation.date for operation in operations])))
            for ticker, operations in operations_by_ticker.items()
        }

        average_price_purchase_for_each_sale_by_ticker = {
            ticker: {
                day: {"position": 0, "operation_type": None,}
                for day in operations_days_by_ticker[ticker]
            }
            for ticker in asset_portfolio
        }

        for ticker, operations in operations_by_ticker.items():
            for day in operations_days_by_ticker[ticker]:
                average_price_purchase_operations_by_ticker = self._calcule_average_purchase_price_certain_day(
                    day, operations, average_price_purchase_for_each_sale_by_ticker,
                )
        return average_price_purchase_operations_by_ticker

    def _calcule_normal_operation_monthly_params(
        self,
        operations: list,
        average_price_by_ticker: dict,
        year_month: str,
        ticker: str,
    ) -> dict:
        """To calcule params of normal operations in a reference year_month, indexed by operation type and ticker"""
        monthly_params = {
            **self._get_last_position_average_price_for_month(
                average_price_by_ticker, year_month
            ),
            **{
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
            },
        }

        for operation in operations:
            operation_month = operation.date.strftime("%m/%Y")
            if operation_month == year_month and operation.ticker == ticker:
                monthly_params["total_amount_" + operation.operation_type] += (
                    operation.amount
                    + (
                        operation.operation_costs
                        * self.mapper_operation_type_factor[operation.operation_type]
                    )
                )
                monthly_params[
                    "total_units_" + operation.operation_type
                ] += operation.units
                if operation.operation_type == "sale":
                    monthly_params["cgs"] += (
                        operation.units * monthly_params["average_purchase_price"]
                    )

        monthly_params["result"] = (
            monthly_params["total_amount_sale"] - monthly_params["cgs"]
        )

        return monthly_params

    def calcule_normal_operations(self, operations: list, **kwargs) -> list:
        tickers = SimpleCappUtils.get_unique_values(operations, "ticker")
        year_months_to_reference_year = self.compile_year_months_reference_year(
            operations[0].date.year
        )

        compile_normal_operations = {
            ticker: {
                year_month: {
                    **self._calcule_normal_operation_monthly_params(
                        operations, kwargs["average_price"][ticker], year_month, ticker
                    ),
                    **{
                        "year_month": year_month,
                        "ticker": ticker,
                        "operation_class": "normal",
                    },
                }
                for year_month in year_months_to_reference_year
            }
            for ticker in tickers
        }

        return SimpleCappUtils.unpack_dict_in_list_of_rows(2, compile_normal_operations)

    def process(self, operations) -> list:
        average_price = self._calcule_average_purchase_price_for_each_sale(operations)
        agrouped_operations_by_ticker_type = self.agroup_operations_by_ticker_type(
            operations, self.mapper_ticker_types.keys()
        )
        sumamary_by_ticker = []
        for (ticker_type, operations) in agrouped_operations_by_ticker_type.items():
            sumamary_by_ticker.extend(
                self.mapper_ticker_types[ticker_type].process(
                    operations, self.calcule_normal_operations, average_price
                )
            )

        return sumamary_by_ticker


class CalculationEngine:
    """Main handler (entrypoint) of calculation engine"""

    model_class = AnnualSummary

    mapper_operation_classes = {
        "day-trade": DayTradeCalculate(),
        "normal": NormalCalculate(),
    }

    def _agroup_operations_by_operation_class(self, operations: list) -> dict:
        """To agroup financial operations by operation class"""
        agrouped_operations_by_operation_class = {
            operation_class: SimpleCappUtils.get_list_with_filters(
                {"operation_class": operation_class}, operations
            )
            for operation_class in self.mapper_operation_classes.keys()
        }

        return agrouped_operations_by_operation_class

    def __init__(self, message: str) -> None:
        try:
            message_dict = json.loads(message)
            self.annual_summary = self.model_class(**message_dict)
        except:
            raise InvalidAnnualSummary()

    def process(self) -> None:
        agrouped_operations_by_operation_class = self._agroup_operations_by_operation_class(
            self.annual_summary.financial_operations
        )

        summary_by_ticker = []
        for (
            operation_class,
            operations,
        ) in agrouped_operations_by_operation_class.items():
            summary_by_ticker.extend(
                self.mapper_operation_classes[operation_class].process(operations)
            )

