# TODO TRATAR LOGS POSIÇÕES NEGATIVAS


# TODO DAQUI P FRENTE: ADICIONAR IRRF VENDA DAY TRADE
# TODO APURAR IMPOSTO A CADA VENDA



from calculation_engine.handler import CalculationEngine

with open('message.json') as message:
    instance_of_calculation = CalculationEngine(message.read())
    instance_of_calculation.process()
