import os

from constants import PHONE_TESTER
from wapchita import Wapchita


def test_send_message_text(wapchita: Wapchita, text_test: str) -> None:
    if not os.getenv("MOCKED_TEST_SEND_MESSAGE"):
        r = wapchita.send_message(phone=PHONE_TESTER, message=text_test)
        assert r.status_code == 201
