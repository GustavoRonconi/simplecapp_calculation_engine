import json


from calculation_engine.exceptions import InvalidAnnualSummary
from calculation_engine.models.annual_summary import AnnualSummary
from calculation_engine.utils import SimpleCappUtils
from calculation_engine.operation_classes import DayTradeCalculate, NormalCalculate


class CalculationEngine:
    """Main handler (entrypoint) of calculation engine"""

    model_class = AnnualSummary

    mapper_operation_classes = {
        "day_trade": DayTradeCalculate,
        "normal": NormalCalculate,
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
        reference_year = self.annual_summary.reference_year
        previous_year_results = self.annual_summary.previous_year_results

        summary_by_ticker, custody_by_ticker_and_reference_year, summary_by_monthly, inconsistencies = (
            [],
            [],
            [],
            [],
        )
        for (operation_class, operations,) in agrouped_operations_by_operation_class.items():
            output_by_operation_class = self.mapper_operation_classes[operation_class]().process(
                operations, reference_year, previous_year_results
            )
            summary_by_ticker.extend(output_by_operation_class["summary_by_ticker"])
            custody_by_ticker_and_reference_year.extend(
                output_by_operation_class["custody_by_ticker_and_reference_year"]
            )
            summary_by_monthly.extend(output_by_operation_class["summary_by_monthly"])
            inconsistencies.extend(output_by_operation_class["inconsistencies"])

        
