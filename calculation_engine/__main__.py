from calculation_engine.handler import CalculationEngine

with open("message.json") as message:
    instance_of_calculation = CalculationEngine(message.read())
    instance_of_calculation.process()
