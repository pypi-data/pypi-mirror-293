import requests
from requests import Response

from wapchita._api.headers import get_headers
from wapchita._api.urls import url_contacts


def contacts(*, tkn: str, device_id: str, phone: str) -> Response:
    url = url_contacts(device_id=device_id, user_wid=phone)
    return requests.get(url=url, headers=get_headers(tkn=tkn))
