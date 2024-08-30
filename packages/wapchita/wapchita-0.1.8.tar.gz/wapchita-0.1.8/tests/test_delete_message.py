from datetime import datetime, UTC

from constants import PHONE_TESTER
from wapchita import Wapchita


def test_delete_message(wapchita: Wapchita):
    response = wapchita.send_message(phone=PHONE_TESTER, message=f"Simple text message to be deleted {datetime.now(tz=UTC)}")
    assert response.status_code == 201
    message_wid = response.json()['waId']
    response = wapchita.delete_message(message_wid=message_wid)
    assert response.status_code == 202
