from calculation_engine.ticker_types.ticker_type_commons import TickerTypesCommons


class BDR(TickerTypesCommons):
    """To handler BDR operations"""

    ticker_type = "bdr"
    exception_sale_limit = 0
    index_ir = 0.2

