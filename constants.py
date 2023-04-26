from enum import Enum


class Markets(Enum):
    BTC = "BTC"
    ETH = "ETH"
    USDT = "USDT"


class Headers(Enum):
    SYMBOL = "Symbol"
    VOLUME = "Volume"
    DEPTH = "Depth"
    PRICE = "Price"
