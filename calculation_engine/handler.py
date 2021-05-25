import json

from calculation_engine.exceptions import InvalidAnnualSummary
from calculation_engine.models.annual_summary import AnnualSummary


class PaperCommons:
    def _get_asset_portfolio(self, operations: list) -> list:
        asset_portfolio = []
        for op in operations:
            if op.paper not in asset_portfolio:
                asset_portfolio.append(op.paper)

        return asset_portfolio

    def agroup_financial_operation_by_paper(self, operations: list) -> dict:
        asset_portfolio = self._get_asset_portfolio(operations)

        agroup_financial_operation_by_paper = {paper: [] for paper in asset_portfolio}
        for op in operations:
            agroup_financial_operation_by_paper[op.paper].append(op)

        return agroup_financial_operation_by_paper


class StocksCalculate(PaperCommons):
    def process(self, operations):
        agroup_financial_operation_by_paper = super().agroup_financial_operation_by_paper(
            operations
        )

        # TODO verificar o calculo de preço médio


class RealStateFundsCalculate(PaperCommons):
    def process(self, operations):
        agroup_financial_operation_by_paper = super().agroup_financial_operation_by_paper(
            operations
        )

        # TODO verificar o calculo de preco médio


class CalculationEngine:
    model_class = AnnualSummary

    mapper_paper_type_classes = {
        "STOKES": StocksCalculate(),
        "FIIs": RealStateFundsCalculate(),
    }

    def __init__(self, message: str) -> None:
        try:
            message_dict = json.loads(message)
            self.annual_summary = self.model_class(**message_dict)
        except:
            raise InvalidAnnualSummary()

    def _agroup_financial_operations_by_paper_types(
        self, financial_operations: list
    ) -> dict:
        agrouped_financial_operations_by_paper_types = {
            paper_type: [] for paper_type in self.mapper_paper_type_classes.keys()
        }
        for op in financial_operations:
            agrouped_financial_operations_by_paper_types[op.paper_type].append(op)

        return agrouped_financial_operations_by_paper_types

    def process(self) -> None:
        agrouped_financial_operations_by_paper_types = self._agroup_financial_operations_by_paper_types(
            self.annual_summary.financial_operations
        )

        for paper_type, operations in agrouped_financial_operations_by_paper_types:
            self.mapper_paper_type_classes[paper_type].process(operations)

