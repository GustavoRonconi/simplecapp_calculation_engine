import json


from calculation_engine.exceptions import InvalidAnnualSummary
from calculation_engine.models.annual_summary import AnnualSummary
from calculation_engine.utils import SimpleCappUtils
from calculation_engine.operation_classes import DayTradeCalculate, NormalCalculate


class CalculationEngine:
    """Main handler (entrypoint) of calculation engine"""

    model_class = AnnualSummary

    mapper_operation_classes = {
        "day_trade": DayTradeCalculate(),
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
        for (operation_class, operations,) in agrouped_operations_by_operation_class.items():
            summary_by_ticker.extend(self.mapper_operation_classes[operation_class].process(operations))

        print(1)
