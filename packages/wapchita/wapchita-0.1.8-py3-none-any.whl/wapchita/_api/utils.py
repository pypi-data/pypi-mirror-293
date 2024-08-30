import asyncio
import time

import httpx
import requests
from requests import Response

from wapchita._api.headers import get_headers
from wapchita._api.urls import url_get_message


def wait_msg_sent(*, tkn: str, message_wid: str) -> Response:
    QUEUED = "queued"  # Status de mensaje en cola.
    url = url_get_message(message_wid=message_wid)
    headers = get_headers(tkn=tkn)
    response = requests.get(url, headers=headers)
    while response.json()["status"] == QUEUED:
        time.sleep(1)
        response = requests.get(url, headers=headers)
    return response


async def async_wait_msg_sent(*, tkn: str, message_wid: str) -> httpx.Response:
    QUEUED = "queued"
    url = url_get_message(message_wid=message_wid)
    headers = get_headers(tkn=tkn)

    async with httpx.AsyncClient() as httpx_client:
        response = await httpx_client.get(url, headers=headers)
        while response.json()["status"] == QUEUED:
            await asyncio.sleep(1)
            response = await httpx_client.get(url, headers=headers)
    return response
