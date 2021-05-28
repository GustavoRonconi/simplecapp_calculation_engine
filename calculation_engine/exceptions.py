class InvalidAnnualSummary(Exception):
    msg = "invalid_annual_summary"


class NoPossivelCalculateAveragePrice(Exception):
    msg = "Não é possível calcular o preço médio, apenas operações de venda"