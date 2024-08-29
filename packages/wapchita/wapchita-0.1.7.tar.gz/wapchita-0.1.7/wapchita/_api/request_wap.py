""" Requests básicas de Wapchita, actualizar al agregar."""
import logging
from pathlib import Path
from typing import List, Optional

from requests import Response

from wapchita.typings import (
    Priority, PRIORITY_DEFAULT,
    SortChats, SORTCHATS_DEFAULT,
    T_KindGroupChats
)
from wapchita.utils import instance_device
from wapchita.models.device import WapDevice
from wapchita._api.endpoints.contacts import contacts
from wapchita._api.endpoints.create_contact import create_contact
from wapchita._api.endpoints.group_chats import group_chats, ResponseGroups
from wapchita._api.endpoints.delete_message import delete_message
from wapchita._api.endpoints.device_by_id import device_by_id
from wapchita._api.endpoints.download_file import download_file
from wapchita._api.endpoints.edit_message import edit_message
from wapchita._api.endpoints.get_chats import get_chats
from wapchita._api.endpoints.search_chat import search_chat
from wapchita._api.endpoints.send_message import send_message
from wapchita._api.endpoints.update_chat_labels import update_chat_labels
from wapchita._api.endpoints.upload_file import upload_file
from wapchita._api.endpoints.mark_as_unread import mark_as_unread
from wapchita._api.endpoints.get_chat_details import get_chat_details

logger = logging.getLogger(__name__)


class RequestWap:
    """ TODO: Encapsular requests con tenacity, de forma que sea flexible."""

    def __init__(self, *, tkn: str, device: WapDevice | str | Path):
        self._tkn = tkn
        self._device: WapDevice = instance_device(tkn=tkn, device=device)

    @property
    def tkn(self) -> str:
        return self._tkn

    @property
    def device(self) -> WapDevice:
        return self._device

    @property
    def device_id(self) -> str:
        return self.device.id

    def contacts(self, phone: str, create_if_404: bool = False) -> Response:
        """ TODO: Documentar: Funciona también con `user_wid`."""
        r = contacts(tkn=self.tkn, device_id=self.device_id, phone=phone)
        if r.status_code == 404 and create_if_404:
            logger.info(f"contacts_404 -> Create contact {phone}.")
            r_create = self.create_contact(phone=phone)
            r = contacts(tkn=self.tkn, device_id=self.device_id, phone=phone)
        return r

    def create_contact(self, *, phone: str, name: Optional[str] = None, surname: Optional[str] = None) -> Response:
        return create_contact(tkn=self.tkn, device_id=self.device_id, phone=phone, name=name, surname=surname)

    def group_chats(self, *, kind: T_KindGroupChats = "any", page: int = 0, size: int = 100) -> Response:
        return group_chats(tkn=self.tkn, device_id=self.device_id, kind=kind, page=page, size=size)

    def device_by_id(self, *, device_id: str) -> Response:
        return device_by_id(tkn=self.tkn, device_id=device_id)

    def download_file(self, *, file_id: str) -> Response:
        return download_file(tkn=self.tkn, device_id=self.device_id, file_id=file_id)

    def edit_message(self, *, message_wid: str, text: str) -> Response:
        return edit_message(tkn=self.tkn, device_id=self.device_id, message_wid=message_wid, text=text)

    def get_chats(self, *, user_wid: str, sort_: SortChats = SORTCHATS_DEFAULT, message_wid: Optional[str] = None) -> Response:
        return get_chats(tkn=self.tkn, device_id=self.device_id, user_wid=user_wid, sort_=sort_, message_wid=message_wid)

    def get_chat_details(self, *, message_wid: str) -> Response:
        return get_chat_details(tkn=self.tkn, device_id=self.device_id, message_wid=message_wid)

    def search_chat(self, *, phone: str, device_id: str) -> Response:
        return search_chat(tkn=self.tkn, phone=phone, device_id=device_id)

    def send_message(self, *, phone: str, message: str = "", file_id: str = None, priority: Priority = PRIORITY_DEFAULT) -> Response:
        return send_message(tkn=self.tkn, phone=phone, message=message, file_id=file_id, priority=priority)

    def update_chat_labels(self, *, user_wid: str, labels: List[str] = None) -> Response:
        return update_chat_labels(tkn=self.tkn, device_id=self.device_id, user_wid=user_wid, labels=labels)

    def upload_file(self, *, path_file: Path) -> Response:
        return upload_file(tkn=self.tkn, path_file=path_file)

    def mark_as_unread(self, *, user_wid: str, unread: bool = True) -> Response:
        return mark_as_unread(tkn=self.tkn, device_id=self.device_id, user_wid=user_wid, unread=unread)

    def delete_message(self, *, message_wid: str) -> Response:
        return delete_message(tkn=self.tkn, message_wid=message_wid)
