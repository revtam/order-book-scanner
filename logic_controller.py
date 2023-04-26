import asyncio
import re

from kucoin_handler import Kucoin_exchange


class Logic_controller:

    def __init__(self, event_loop=None):
        self.kucoin = Kucoin_exchange()
        if event_loop:
            self._loop = event_loop
        else:
            self._loop = asyncio.get_event_loop()
        self._latest_table_data = None

    def get_last_table_data(self):
        return self._latest_table_data

    def load_table_data(self, markets, depth_percent):
        """
            @params markets: list of markets e.g. BTC, ETH
            @return 
        """
        tickers = self.kucoin.get_all_tickers()
        selected_markets_tickers_dict = {each_ticker.get_name(): each_ticker for each_ticker in tickers if re.match(
            f".*-({'|'.join(markets)})", each_ticker.get_name())}

        # order_books_list = self._collect_depths(
        #     selected_markets_tickers_dict.keys(), depth_percent)
        order_books_list = self._collect_depths_seq(
            selected_markets_tickers_dict.keys(), depth_percent)

        for symbol, depth in order_books_list:
            selected_markets_tickers_dict[symbol].set_depth(depth)

        self._latest_table_data = [
            elem for elem in selected_markets_tickers_dict.values()]
        return self._latest_table_data

    def sort_by_symbol(self, tickers_list):
        self._sort(tickers_list, lambda ticker: ticker.get_name())

    def sort_by_volume(self, tickers_list):
        self._sort(tickers_list, lambda ticker: ticker.get_volume())

    def sort_by_depth(self, tickers_list):
        self._sort(tickers_list, lambda ticker: ticker.get_depth())

    def sort_by_price(self, tickers_list):
        self._sort(tickers_list, lambda ticker: ticker.get_price())

    @staticmethod
    def _sort(tickers_list, key_lambda):
        tickers_list.sort(key=key_lambda, reverse=False)

    @staticmethod
    def _get_total_bid_amount(order_book, depth_percent):
        bids = order_book["bids"]
        if bids is None:
            return None
        highest_bid = float(bids[0][0])
        last_bid_in_depth = highest_bid * (100 - depth_percent) / 100
        depth_sum = 0
        for price, amount in bids:
            if float(price) < last_bid_in_depth:
                break
            depth_sum += float(amount) * float(price)
        return depth_sum

    def _collect_depths(self, symbols_list, depth_percent):
        symbols_list = [symbol for symbol in symbols_list]
        # symbols_list = symbols_list[:30]
        return self._loop.run_until_complete(self._async_depth_collecting(symbols_list, depth_percent))

    def _collect_depths_seq(self, symbols_list, depth_percent):
        symbols_list = [symbol for symbol in symbols_list]
        total = len(symbols_list)
        results = []
        for i, symbol in enumerate(symbols_list, 1):
            total_bid_amount = self._get_total_bid_amount(
                self.kucoin.get_order_book(symbol), depth_percent)
            if total_bid_amount is not None:
                results.append((symbol, total_bid_amount))
            print(f"{i}/{total}")
        return results

    async def _async_depth_collecting(self, symbols_list, depth_percent):
        tasks = [self._async_get_depth(symbol, depth_percent)
                 for symbol in symbols_list]
        return await asyncio.gather(*tasks)

    async def _async_get_depth(self, symbol, depth_percent):
        order_book = await self.kucoin.async_get_order_book(symbol)
        depth = self._get_total_bid_amount(order_book, depth_percent)
        return symbol, depth
