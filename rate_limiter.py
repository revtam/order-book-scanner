import time


class Rate_limiter:

    def __init__(self, limit, intervall):
        """
            @params limit: max number of requests in a given intervall, intervall: time intervall in seconds
        """
        self.__limit = limit
        self.__intervall = intervall
        self.__counter = 0
        self.__intervall_start = 0

    def call(self, method_to_call, *args):
        """
            Calls method as soon as possible
        """
        this_call_time = time.time()
        if this_call_time - self.__intervall_start >= self.__intervall:
            self.__intervall_start = this_call_time
            self.__counter = 0
        self.__counter += 1
        self._wait_till_call()
        return method_to_call(*args)

    def _wait_till_call(self):
        if self.__counter < self.__limit:
            return
        time.sleep(self.__intervall_start + self.__intervall - time.time())
