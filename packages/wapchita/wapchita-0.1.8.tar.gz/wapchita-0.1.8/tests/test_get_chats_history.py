import os
import asyncio

from constants import PHONE_TESTER
from wapchita import Wapchita, WapChat, phone2wid


def test_get_chats_history(wapchita: Wapchita):
    chats_response = asyncio.run(wapchita.async_get_chats_history(
        user_wid=phone2wid(phone=PHONE_TESTER),
        message_wid=os.getenv("EXAMPLE_MESSAGE_WID"))
    )
    assert isinstance(chats_response, list)
    assert len(chats_response) > 0
    assert isinstance(chats_response[0], WapChat)


def test_get_chats_history_olders_first(wapchita: Wapchita):
    chats_response = asyncio.run(wapchita.async_get_chats_history(
        user_wid=phone2wid(phone=PHONE_TESTER),
        message_wid=os.getenv("EXAMPLE_MESSAGE_WID"))
    )
    # The last is our current message
    assert chats_response[-1].id == os.getenv("EXAMPLE_MESSAGE_WID")
