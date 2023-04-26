class Ticker:

    def __init__(self, name, last_price, volume):
        """
            @params symbol name, last traded price, 24h volume
        """
        self._name = name
        self._last_price = last_price
        self._volume = volume
        self._depth = 0

    def get_name(self):
        return self._name

    def get_price(self):
        return self._last_price

    def get_volume(self):
        return self._volume

    def set_depth(self, depth):
        self._depth = depth

    def get_depth(self):
        return self._depth
