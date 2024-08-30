import requests
from requests import Response

from wapchita._api.headers import get_headers
from wapchita._api.urls import url_device_by_id


def device_by_id(*, tkn: str, device_id: str) -> Response:
    url = url_device_by_id(device_id=device_id)
    return requests.get(url=url, headers=get_headers(tkn=tkn))
