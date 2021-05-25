import json

from calculation_engine.exceptions import InvalidAnnualSummary
from calculation_engine.models.annual_summary import AnnualSummary


class CalculationEngine():
    model_class = AnnualSummary

    def __init__(self, message: str) -> None:
        try:
            message_dict = json.loads(message)
            self.annual_summary = self.model_class(**message_dict)
        except:
            raise InvalidAnnualSummary()
        

    def process(self) -> None:
        print(1)
