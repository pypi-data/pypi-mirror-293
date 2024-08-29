import os

from constants import PHONE_TESTER
from wapchita import Wapchita, phone2wid


def test_get_chats_with_messages(wapchita: Wapchita):
    chats_response = wapchita.get_chats(user_wid=phone2wid(phone=PHONE_TESTER))
    assert chats_response.status_code == 200
    assert PHONE_TESTER in chats_response.text
    chats = chats_response.json()
    assert isinstance(chats, list)
    assert len(chats) > 0


def test_get_chats_with_wrong_number(wapchita: Wapchita):
    chats_response = wapchita.get_chats(user_wid='asdasdasd')
    assert chats_response.status_code == 200
    assert len(chats_response.json()) == 0


def test_get_chats_with_real_message_wid(wapchita: Wapchita):
    chats_response = wapchita.get_chats(user_wid=phone2wid(phone=PHONE_TESTER), message_wid=os.getenv("EXAMPLE_MESSAGE_WID"))
    assert chats_response.status_code == 200
    assert isinstance(chats_response.json(), list)
    assert len(chats_response.json()) > 0


def test_get_chats_with_wrong_message_wid(wapchita: Wapchita):
    chats_response = wapchita.get_chats(user_wid=phone2wid(phone=PHONE_TESTER), message_wid='idkahj8c98aymsd91muw')
    assert chats_response.status_code in [400, 409]
