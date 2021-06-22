from calculation_engine.ticker_types.ticker_type_commons import \
    TickerTypesCommons


class RealStateFunds(TickerTypesCommons):
    """To handler real state funds operations"""

    ticker_type = "fiis"
    exception_sale_limit = 0
    index_ir = 0.2
