from abc import ABC, abstractmethod


class Exchange(ABC):

    @abstractmethod
    def get_all_tickers(self):
        """
            Returns all symbols, last price, 24h volume in quote currency
        """
        pass

    @abstractmethod
    def get_order_book(self, symbol):
        """
            Returns aggregated order book data of given symbol
        """
        pass
