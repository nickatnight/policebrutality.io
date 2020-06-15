import logging
from typing import Union, Dict, List

import requests


def format_json_response(data: List[Dict]) -> Dict:
    """
    {
        "count": 846,
        "data": [
            {
                "city": "Minneapolis"
                "link": "reddit.com",
                "state": "MN",
                "title": "I cant breathe"
            },
            ...
        ]
    }
    :param data:        list of serialized Video objects
    :return:            dict for frontend
    """
    payload = dict()
    payload["count"] = len(data)
    payload["data"] = data

    return payload


class LogHandler(object):
    """base log handler for all external api calls which sets log by class name
    """

    def __init__(self, *args: str, **kwargs: int) -> None:
        self.logger = logging.getLogger(self.__class__.__name__)


class RequestAPI(LogHandler):
    """for making external api requests
    """

    def __init__(self) -> None:
        super().__init__()

    def request(
        self, url: str, method: str = "get", data: Dict = None, **kwargs: int
    ) -> Union[None, requests.Response]:
        """send request

        :param url:             url
        :param method:          request method
        :param data:            data is POST
        :return:                request object, none otherwise
        """
        data = data or {}
        req_to_call = getattr(requests, method)

        try:
            req = req_to_call(url, data, **kwargs)
            req.raise_for_status()
        except requests.exceptions.HTTPError as http_err:
            self.logger.error(str(http_err))
        except Exception as err:
            self.logger.error(f"Other error occurred when making request: {err}.")
        else:
            return req

        return None
