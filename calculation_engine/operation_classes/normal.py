import calendar
from datetime import date

from calculation_engine.operation_classes.operation_classes_commons import \
    OperationClassesCommons
from calculation_engine.utils import SimpleCappUtils


class NormalCalculate(OperationClassesCommons):
    """To hander normal financial operation class"""

    operation_class = "normal"

    def _get_last_position_average_price_for_month(
        self, average_price_by_ticker: dict, year_month: str, ticker: str
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
            if average_price_default["position"] < 0:
                self.append_inconsistency(
                    (
                        f"""Inconsistência encontrada p/ o ticker {ticker}, posição negativa {average_price_default["position"]}, """
                        "certifique-se de que os lançamentos de compra foram processados"
                    )
                )
                return
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

                # APPLY POSITION
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
        last_position = self._get_last_position_average_price_for_month(
            average_price_by_ticker, year_month, ticker
        )
        if not last_position:
            return

        monthly_params = {
            **last_position,
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

    def _calcule_operations_by_ticker(
        self, operations: list, reference_year: int, year_months_to_reference_year: list, **kwargs
    ) -> dict:
        tickers = SimpleCappUtils.get_unique_values(operations, "ticker")
        summary_by_ticker, custody_by_ticker_and_reference_year = {}, {}
        for ticker in tickers:
            summary_by_ticker[ticker] = {}
            custody_by_ticker_and_reference_year[ticker] = {}
            for year_month in year_months_to_reference_year:
                normal_operation_monthly_params = self._calcule_normal_operation_monthly_params(
                    operations, kwargs["average_price"][ticker], year_month, ticker
                )
                if not normal_operation_monthly_params:
                    del summary_by_ticker[ticker], custody_by_ticker_and_reference_year[ticker]
                    break
                summary_by_ticker[ticker][year_month] = {
                    "year_month": year_month,
                    "broker": None,
                    "ticker_type": self.ticker_type_instance.ticker_type,
                    "ticker": ticker,
                    "operation_class": self.operation_class,
                    **normal_operation_monthly_params,
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
