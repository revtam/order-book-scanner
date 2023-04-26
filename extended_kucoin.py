import base64
import hashlib
import hmac
import json
import time
from urllib.parse import urljoin

import aiohttp
from kucoin.market.market import MarketData


class Extended_kucoin_market(MarketData):
    """
        Kucoin Market extended with async http request
    """

    async def async_get_aggregated_orderv3(self, symbol):
        params = {
            'symbol': symbol
        }
        response = await self._async_request('GET', '/api/v3/market/orderbook/level2', params=params)
        return response

    async def _async_request(self, method, uri, timeout=5, auth=True, params=None):
        uri_path = uri
        data_json = ''
        version = 'v1.0.7'
        if method in ['GET', 'DELETE']:
            if params:
                strl = []
                for key in sorted(params):
                    strl.append("{}={}".format(key, params[key]))
                data_json += '&'.join(strl)
                uri += '?' + data_json
                uri_path = uri
        else:
            if params:
                data_json = json.dumps(params)

                uri_path = uri + data_json

        headers = {}
        if auth:
            now_time = int(time.time()) * 1000
            str_to_sign = str(now_time) + method + uri_path
            sign = base64.b64encode(
                hmac.new(self.secret.encode('utf-8'), str_to_sign.encode('utf-8'), hashlib.sha256).digest()).decode("utf-8")
            if self.is_v1api:
                headers = {
                    "KC-API-SIGN": sign,
                    "KC-API-TIMESTAMP": str(now_time),
                    "KC-API-KEY": self.key,
                    "KC-API-PASSPHRASE": self.passphrase,
                    "Content-Type": "application/json"
                }
            else:
                passphrase = base64.b64encode(
                    hmac.new(self.secret.encode('utf-8'), self.passphrase.encode('utf-8'), hashlib.sha256).digest()).decode("utf-8")
                headers = {
                    "KC-API-SIGN": sign,
                    "KC-API-TIMESTAMP": str(now_time),
                    "KC-API-KEY": self.key,
                    "KC-API-PASSPHRASE": passphrase,
                    "Content-Type": "application/json",
                    "KC-API-KEY-VERSION": "2"
                }
        headers["User-Agent"] = "kucoin-python-sdk/"+version
        url = urljoin(self.url, uri)

        class Custom_response:
            """
                Transforms aiohttp library's ClientResponse object to a custom response object 
                for methods that use requests library's Response object
            """

            def __init__(self, status, text):
                self.status_code = status
                self.text = text
                self.content = text  # content is expected to be bytes but here it is just string

            def json(self):
                return json.loads(self.text)

        async with aiohttp.ClientSession() as session:
            if method in ['GET', 'DELETE']:
                async with session.request(method, url, headers=headers, timeout=timeout) as response:
                    response_data = Custom_response(response.status, await response.text())
            else:
                async with session.request(method, url, headers=headers, data=data_json, timeout=timeout) as response:
                    response_data = Custom_response(response.status, await response.text())
        return self.check_response_data(response_data)
