from ib.ext.Contract import Contract


class ContractMixin(object):
    """Contract Mixin Class"""

    def create_contract(self, symbol):
        """Create an Interactive Brokers contract object. This specifies the
        equity type, the exchange, the currency, and the symbol to trade.
        """
        c = Contract()
        c.m_symbol = symbol
        c.m_secType = "STK"
        c.m_exchange = "SMART"
        c.m_primaryExch = "SMART"
        c.m_currency = "USD"
        return c
