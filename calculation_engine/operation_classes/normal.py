import calendar
from datetime import date

from calculation_engine.finops_commons import FinopsCommons
from calculation_engine.utils import SimpleCappUtils


class NormalCalculate(FinopsCommons):
    """To hander normal financial operation class"""

    def _get_last_position_average_price_for_month(
        self, average_price_by_ticker: dict, year_month: str
    ) -> dict:
        """To get a last position and average price for a specific month"""
        month, year = year_month.split("/")
        max_date = date(int(year), int(month), calendar.monthrange(int(year), int(month))[1])
        last_date = list(average_price_by_ticker.keys())[0]
        average_price_default = average_price_by_ticker[last_date]

        for reference_date, average_price in average_price_by_ticker.items():
            if reference_date <= max_date:
                average_price.pop("total_amount_with_operation_costs", None)
                average_price.pop("operation_type", None)
                average_price_default = average_price
                last_date = reference_date

        if last_date <= max_date:
            return average_price_default

        return {"position": 0.0, "average_purchase_price": 0.0}

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
                ] = mapper_math_operations_by_operation_type[operation.operation_type.value](
                    average_price_ticket[operation.ticker][day]["position"], operation.units,
                )

                # CONDITION AVERAGE PRICE
                if operation.operation_type.value == "purchase":
                    amount_to_calc_average_price = mapper_math_operations_by_operation_type[
                        operation.operation_type.value
                    ](amount_to_calc_average_price, operation.amount, operation.operation_costs,)
                    position_to_calc_average_price = mapper_math_operations_by_operation_type[
                        operation.operation_type.value
                    ](position_to_calc_average_price, operation.units)

            if operation.date == day:
                average_price_ticket[operation.ticker][day]["operation_type"] = operation.operation_type.value
                if position_to_calc_average_price <= 0:
                    average_price_ticket[operation.ticker][day]["average_purchase_price"] = None
                    continue
                average_price_ticket[operation.ticker][day]["average_purchase_price"] = (
                    amount_to_calc_average_price / position_to_calc_average_price
                )

        return average_price_ticket

    def _calcule_average_purchase_price_for_each_sale(self, operations: list) -> dict:
        """To calcule average purchase price for each sale operation"""

        ordered_operations = sorted(operations, key=lambda x: x.date)

        asset_portfolio = SimpleCappUtils.get_unique_values(ordered_operations, "ticker")

        operations_by_ticker = SimpleCappUtils.index_list_by_list_of_keys(
            ordered_operations, asset_portfolio, "ticker"
        )

        operations_days_by_ticker = {
            ticker: sorted(list(set([operation.date for operation in operations])))
            for ticker, operations in operations_by_ticker.items()
        }

        average_price_purchase_for_each_sale_by_ticker = {
            ticker: {
                day: {"position": 0, "operation_type": None,} for day in operations_days_by_ticker[ticker]
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
        self, operations: list, average_price_by_ticker: dict, year_month: str, ticker: str,
    ) -> dict:
        """To calcule params of normal operations in a reference year_month, indexed by operation type and ticker"""
        monthly_params = {
            **self._get_last_position_average_price_for_month(average_price_by_ticker, year_month),
            **{
                "total_amount_purchase": 0,
                "total_amount_sale": 0,
                "total_units_purchase": 0,
                "total_units_sale": 0,
                "cgs": 0,
                "irrf": 0,
            },
        }

        for operation in operations:
            operation_month = operation.date.strftime("%m/%Y")
            if operation_month == year_month and operation.ticker == ticker:
                monthly_params["total_amount_" + operation.operation_type.value] += operation.amount + (
                    operation.operation_costs
                    * self.mapper_operation_type_factor[operation.operation_type.value]
                )
                monthly_params["total_units_" + operation.operation_type.value] += operation.units
                monthly_params["irrf"] += operation.irrf
                if operation.operation_type.value == "sale":
                    monthly_params["cgs"] += operation.units * monthly_params["average_purchase_price"]

        monthly_params["result"] = monthly_params["total_amount_sale"] - monthly_params["cgs"]

        return monthly_params

    def calcule_normal_operations(self, operations: list, reference_year: int, **kwargs) -> dict:
        tickers = SimpleCappUtils.get_unique_values(operations, "ticker")
        year_months_to_reference_year = self.compile_year_months_reference_year(reference_year)

        summary_by_ticker, custody_by_ticker_and_reference_year = {}, {}
        for ticker in tickers:
            summary_by_ticker[ticker] = {}
            custody_by_ticker_and_reference_year[ticker] = {}
            for year_month in year_months_to_reference_year:
                summary_by_ticker[ticker][year_month] = {
                    **{
                        "year_month": year_month,
                        "broker": None,
                        "ticker": ticker,
                        "operation_class": "normal",
                    },
                    **self._calcule_normal_operation_monthly_params(
                        operations, kwargs["average_price"][ticker], year_month, ticker
                    ),
                }

                if year_month == f"12/{reference_year}":
                    custody_by_ticker_and_reference_year[ticker][year_month] = {
                        "ticker": ticker,
                        "year_month": year_month,
                        "position": summary_by_ticker[ticker][year_month]["position"],
                        "average_purchase_price": summary_by_ticker[ticker][year_month][
                            "average_purchase_price"
                        ],
                        "total_amount": (
                            summary_by_ticker[ticker][year_month]["position"]
                            * summary_by_ticker[ticker][year_month]["average_purchase_price"]
                        ),
                    }

        return {
            "summary_by_ticker": SimpleCappUtils.unpack_dict_in_list_of_rows(2, summary_by_ticker),
            "custody_by_ticker_and_reference_year": SimpleCappUtils.unpack_dict_in_list_of_rows(
                2, custody_by_ticker_and_reference_year
            ),
        }

    def process(self, operations: list, reference_year: int) -> dict:
        if not operations:
            return {"summary_by_ticker": [], "custody_by_ticker_and_reference_year": []}
        average_price = self._calcule_average_purchase_price_for_each_sale(operations)
        agrouped_operations_by_ticker_type = self.agroup_operations_by_ticker_type(operations)
        output_by_operation_class = {"summary_by_ticker": [], "custody_by_ticker_and_reference_year": []}

        for (ticker_type, operations) in agrouped_operations_by_ticker_type.items():
            output_by_ticker_type = self.mapper_ticker_types[ticker_type].process(
                operations, reference_year, self.calcule_normal_operations, average_price
            )
            output_by_operation_class["summary_by_ticker"].extend(output_by_ticker_type["summary_by_ticker"])
            output_by_operation_class["custody_by_ticker_and_reference_year"].extend(
                output_by_ticker_type["custody_by_ticker_and_reference_year"]
            )

        return output_by_operation_class
