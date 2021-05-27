import json
from datetime import date

from calculation_engine.exceptions import InvalidAnnualSummary
from calculation_engine.models.annual_summary import AnnualSummary
from calculation_engine.utils import SimpleCappUtils


class FinopsCommons:
    """Commons operations to all financial operations"""

    def _calcule_average_purchase_price_by_ticker_day(
        self,
        day: date,
        finantial_operations_by_ticket: list,
        average_price_ticket: dict,
    ):
        """To calculate average price """
        for index, fin_op in enumerate(finantial_operations_by_ticket, 1):
            if fin_op.date <= day:
                average_price_ticket[fin_op.ticker][day]["total_units"] += fin_op.units
                average_price_ticket[fin_op.ticker][day][
                    "total_amount_with_emoluments"
                ] = (
                    average_price_ticket[fin_op.ticker][day][
                        "total_amount_with_emoluments"
                    ]
                    + fin_op.amount
                    + fin_op.emoluments
                )
            if index == len(finantial_operations_by_ticket):
                if average_price_ticket[fin_op.ticker][day]["total_units"] == 0:
                    del average_price_ticket[fin_op.ticker][day]
                    continue

                average_price_ticket[fin_op.ticker][day]["average_price"] = (
                    average_price_ticket[fin_op.ticker][day][
                        "total_amount_with_emoluments"
                    ]
                    / average_price_ticket[fin_op.ticker][day]["total_units"]
                )
        return average_price_ticket

    def agroup_financial_operations_by_operation_type(
        self, financial_operations: list
    ) -> dict:
        """To agroup financial operations by operation type"""
        agrouped_financial_operations_by_operation_type = {
            operation_type: SimpleCappUtils.get_list_with_filters(
                {"operation_type": operation_type}, financial_operations
            )
            for operation_type in self.mapper_ticker_classes.keys()
        }

    def agroup_financial_operations_by_operation_class(
        self, financial_operations: list
    ) -> dict:
        """To agroup financial operations by operation class"""
        agrouped_financial_operations_by_operation_class = {
            operation_class: SimpleCappUtils.get_list_with_filters(
                {"operation_class": operation_class}, financial_operations
            )
            for operation_class in self.mapper_ticker_classes.keys()
        }

        return agrouped_financial_operations_by_operation_class

    def calcule_average_purchase_price(self, financial_operations: list) -> dict:
        """To calcule average purchase price to operations by ticker until the referenced date"""
        purchase_financial_operations = SimpleCappUtils.get_list_with_filters(
            {"operation_type": "purchase"}, financial_operations,
        )
        purchase_asset_portfolio = SimpleCappUtils.get_unique_values(
            purchase_financial_operations, "ticker"
        )

        purchase_financial_operations_by_tiker = SimpleCappUtils.index_list_by_list_of_keys(
            purchase_financial_operations, purchase_asset_portfolio, "ticker"
        )

        purchase_operation_days = sorted(
            SimpleCappUtils.get_unique_values(purchase_financial_operations, "date")
        )
        average_price_purchase_operations_by_ticker = {
            ticker: {
                date: {"total_units": 0, "total_amount_with_emoluments": 0}
                for date in purchase_operation_days
            }
            for ticker in purchase_asset_portfolio
        }

        for day in purchase_operation_days:
            for (
                purchase_financial_operations
            ) in purchase_financial_operations_by_tiker.values():
                average_price_purchase_operations_by_ticker = self._calcule_average_purchase_price_by_ticker_day(
                    day,
                    purchase_financial_operations,
                    average_price_purchase_operations_by_ticker,
                )

        return average_price_purchase_operations_by_ticker

    def calcule_sales_profit_loss(self, operation: dict, average_price: dict) -> list:
        return (operation.amount + operation.emoluments) - average_price[operation.date]


class RealStateFunds(FinopsCommons):
    """To handler real state funds operations"""
    def _get_unique_year_months(operations: list) -> list:
        """To get a unique year months"""
        year_months = []
        for op in operations:
            year_month = str(op.date.year) + str(op.date.month)
            if year_month not in year_months:
                year_months.append(year_month)
        
        return year_months
    
    def _get_last_position_in_month(averege_price_by_dict):
        pass

    def _process_normal_operations(self, operations: list, average_price: dict) -> list:
        tickers = SimpleCappUtils.get_unique_values(operations, 'ticker')
        year_month = self._get_unique_year_months(operations)

        compile_normal_operations = {ticket: {year: {"position": 0, "average_price": average_price[ticket][]} for year in year_month} for ticket in tickers}

        for op in operations:
            year_month = str(op.date.year) + str(op.date.month)
            



    def _process_day_trade_operations(operations: list) -> list:
        return []

    def process(
        self,
        operations: list,
        operation_class: str,
        average_price: dict = None,
        purchase_day_price: dict = None,
    ) -> dict:
        sumamary_by_ticker = []

        if operation_class == "normal":
            self._process_normal_operations()

        elif operation_class == "day_trade":
            self._process_day_trade_operations()

        return sumamary_by_ticker


class Stock(FinopsCommons):
    """To handler stook operations"""

    def process(self, operations, operation_class: str) -> dict:
        return []


class BDR(FinopsCommons):
    """To handler stook operations"""

    pass


class DayTradeCalculate(FinopsCommons):
    """To hander day-trade financial operation classess"""

    operation_class = "day-trade"

    mapper_operation_types = {
        "fiis": RealStateFunds(),
        "stook": Stock(),
        "bdr": BDR(),
    }

    def process(self, operations) -> list:
        return []


class NormalCalculate(FinopsCommons):
    """To hander normal financial operation classes"""

    operation_class = "normal"

    mapper_operation_types = {
        "fiis": RealStateFunds(),
        "stook": Stock(),
        "bdr": BDR(),
    }

    def process(self, operations) -> list:
        average_price = self.calcule_average_purchase_price(operations)
        agrouped_financial_operations_by_operation_type = self.agroup_financial_operations_by_operation_type(
            operations
        )
        sumamary_by_ticker = []
        for (
            operation_type,
            operations,
        ) in agrouped_financial_operations_by_operation_type.items():
            sumamary_by_ticker.extend(
                self.mapper_operation_types[operation_type].process(
                    operations, self.operation_class, average_price
                )
            )

        return sumamary_by_ticker


class CalculationEngine(FinopsCommons):
    """Main handler (entrypoint) of calculation engine"""

    model_class = AnnualSummary

    mapper_operation_classes = {
        "day-trade": DayTradeCalculate(),
        "normal": NormalCalculate(),
    }

    def __init__(self, message: str) -> None:
        try:
            message_dict = json.loads(message)
            self.annual_summary = self.model_class(**message_dict)
        except:
            raise InvalidAnnualSummary()

    def process(self) -> None:
        agrouped_financial_operations_by_operation_class = self.agroup_financial_operations_by_operation_class(
            self.annual_summary.financial_operations
        )

        summary_by_ticker = []
        for (
            operation_class,
            finantial_operations,
        ) in agrouped_financial_operations_by_operation_class.items():
            summary_by_ticker.extend(
                self.mapper_operation_classes[operation_class].process(
                    finantial_operations
                )
            )

        print(1)
