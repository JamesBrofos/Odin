from ..params.odin_enum import OdinEnum


class Indices(OdinEnum):
    """Odin Financial Indices

    This file contains the tickers of common stock market indices for use in
    trading strategies that may wish to invest idle capital in an index, to
    generate signals relative to an index, or to simply trade the index
    generally.
    """
    # These are the actual indices and they are not tradeable.
    sp_100 = "^OEX"
    sp_500 = "^GSPC"
    # Exchange traded funds that track the indices and are tradeable.
    sp_100_etf = "OEF"
    sp_500_etf = "SPY"

# Define a tuple of assets that cannot be bought.
untradeable_assets = [Indices.sp_100.value, Indices.sp_500.value]
