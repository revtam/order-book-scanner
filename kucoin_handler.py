from extended_kucoin import Extended_kucoin_market

from exchange_interface import Exchange
from rate_limiter import Rate_limiter
from secrets_manager import Api_keys
from ticker import Ticker


class Kucoin_exchange(Exchange):

    def __init__(self):
        self.basic_rate_limiter = Rate_limiter(1800, 60)
        self.strict_rate_limiter = Rate_limiter(20, 3)
        self.client = Extended_kucoin_market(key=Api_keys.kucoin_public,
                                             secret=Api_keys.kucoin_private, passphrase=Api_keys.kucoin_passphrase)

    def get_all_tickers(self):
        return [Ticker(each_ticker["symbol"], each_ticker["last"], each_ticker["volValue"])
                for each_ticker in self.client.get_all_tickers()["ticker"]]

    def get_order_book(self, symbol):
        return self.strict_rate_limiter.call(self.client.get_aggregated_orderv3, symbol)

    async def async_get_order_book(self, symbol):
        """
            @return (symbol, order book) tuple
        """
        print(symbol)
        return await self.strict_rate_limiter.call(self.client.async_get_aggregated_orderv3, symbol)
