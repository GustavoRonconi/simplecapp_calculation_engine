from calculation_engine.ticker_types.ticker_type_commons import TickerTypesCommons


class Stock(TickerTypesCommons):
    """To handler stock operations"""

    ticker_type = "stock"
    exception_sale_limit = 20000
    index_ir = 0.2

