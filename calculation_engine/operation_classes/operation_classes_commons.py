from datetime import datetime

from dateutil import relativedelta

from calculation_engine.ticker_types import BDR, RealStateFunds, Stock
from calculation_engine.utils import SimpleCappUtils


class OperationClassesCommons:
    """Commons operations to all financial operations classes"""

    inconsistencies = []

    mapper_ticker_types = {
        "fiis": RealStateFunds,
        "stock": Stock,
        "bdr": BDR,
    }

    mapper_operation_type_factor = {"sale": -1, "purchase": 1}

    def append_inconsistency(self, message: str):
        """To append inconsistency message in inconsistencies list"""
        if message not in self.inconsistencies:
            self.inconsistencies.append(message)

    def agroup_operations_by_ticker_type(self, operations: list) -> dict:
        """To agroup financial operations by ticker type"""
        agrouped_operations_by_ticker_type = {
            ticker_type: SimpleCappUtils.get_list_with_filters({"ticker_type": ticker_type}, operations)
            for ticker_type in self.mapper_ticker_types.keys()
        }

        return agrouped_operations_by_ticker_type

    def compile_year_months_reference_year(self, reference_year: int) -> list:
        """To compile a list of years_months based in reference year"""
        return [f"{i:02d}/{reference_year}" for i in range(1, 13)]

    def _calcule_operations_by_monthly(
        self,
        summary_by_ticker: list,
        reference_year: int,
        year_months_to_reference_year: list,
        previous_year_loss: list,
    ) -> dict:
        """To compile operations by monthly"""
        summary_by_monthly = {}
        for year_month in year_months_to_reference_year:
            summary_by_monthly[year_month] = {
                "year_month": year_month,
                "ticker_type": self.ticker_type_instance.ticker_type,
                "operation_class": self.operation_class,
            }
            total_amount_sale, result, irrf, accumulated_loss = 0, 0, 0, 0
            for operation in summary_by_ticker:
                if operation["year_month"] == year_month:
                    total_amount_sale += operation["total_amount_sale"]
                    result += operation["result"]
                    irrf += operation["irrf"]

            ir_flag = (
                self.ticker_type_instance.get_ir_flag(total_amount_sale)
                if self.operation_class == "normal"
                else True
            )
            if year_month == f"01/{reference_year}":
                accumulated_loss = sum(
                    (
                        loss.accumulated_loss
                        for loss in previous_year_loss
                        if loss.operation_class == self.operation_class
                        and loss.ticker_type == self.ticker_type_instance.ticker_type
                    )
                )

            elif ir_flag:
                accumulated_loss += result
            if accumulated_loss > 0:
                accumulated_loss = 0
            ir_to_pay = (
                self.ticker_type_instance.calcule_ir_to_pay(result, accumulated_loss, irrf) if ir_flag else 0
            )
            summary_by_monthly[year_month].update(
                {
                    "total_amount_sale": total_amount_sale,
                    "ir_flag": ir_flag,
                    "result": result,
                    "accumulated_loss": accumulated_loss,
                    "irrf": irrf,
                    "ir_to_pay": ir_to_pay,
                    "final_result": result - ir_to_pay,
                }
            )
        return {"summary_by_monthly": SimpleCappUtils.unpack_dict_in_list_of_rows(1, summary_by_monthly)}

    def calcule_operations(
        self, operations: list, reference_year: int, previous_year_loss: list, **kwargs
    ) -> dict:
        year_months_to_reference_year = self.compile_year_months_reference_year(reference_year)

        output_operations_by_ticker = self._calcule_operations_by_ticker(
            operations, reference_year, year_months_to_reference_year, **kwargs
        )

        output_operations_by_monthly = self._calcule_operations_by_monthly(
            output_operations_by_ticker["summary_by_ticker"],
            reference_year,
            year_months_to_reference_year,
            previous_year_loss,
        )

        return {**output_operations_by_ticker, **output_operations_by_monthly}

    def process(self, operations: list, reference_year: int, previous_year_loss: list) -> dict:
        if not operations:
            return {
                "summary_by_ticker": [],
                "custody_by_ticker_and_reference_year": [],
                "summary_by_monthly": [],
            }
        average_price = {}
        if self.operation_class == "normal":
            average_price = self._calcule_average_purchase_price_for_each_sale(operations)
        agrouped_operations_by_ticker_type = self.agroup_operations_by_ticker_type(operations)
        output_by_operation_class = {
            "summary_by_ticker": [],
            "custody_by_ticker_and_reference_year": [],
            "summary_by_monthly": [],
        }

        for (ticker_type, operations) in agrouped_operations_by_ticker_type.items():
            self.ticker_type_instance = self.mapper_ticker_types[ticker_type]()
            output_by_ticker_type = self.ticker_type_instance.process(
                operations, reference_year, previous_year_loss, self.calcule_operations, average_price,
            )
            output_by_operation_class["summary_by_ticker"].extend(output_by_ticker_type["summary_by_ticker"])
            output_by_operation_class["custody_by_ticker_and_reference_year"].extend(
                output_by_ticker_type["custody_by_ticker_and_reference_year"]
            )
            output_by_operation_class["summary_by_monthly"].extend(
                output_by_ticker_type["summary_by_monthly"]
            )

        output_by_operation_class["inconsistencies"] = self.inconsistencies

        return output_by_operation_class
