from constants import PHONE_TESTER
from wapchita import Wapchita, WapUser


def test_get_user(wapchita: Wapchita) -> None:
    user = wapchita.user_from_phone(phone=PHONE_TESTER)
    assert isinstance(user, WapUser) and user.phone == PHONE_TESTER
 