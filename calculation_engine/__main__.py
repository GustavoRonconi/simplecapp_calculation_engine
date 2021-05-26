# TODO verificar com o pessoal a nomenclatura das chaves das mensagens
# TODO verificar com o pessoal o significado do tipo do mercado e as conversoes de especificacao de titulo das notas
# TODO trabalhar com um modelo de recalculo anual e um modelo incrementador na API
# TODO validar o conceito de resumo anual
# TODO para fundos imobiliarios sempre aplica o imposto?
# TODO verificar para qual período devo realizar a apuração (mensal/anual)?



from calculation_engine.handler import CalculationEngine

with open('message.json') as message:
    instance_of_calculation = CalculationEngine(message.read())
    instance_of_calculation.process()
