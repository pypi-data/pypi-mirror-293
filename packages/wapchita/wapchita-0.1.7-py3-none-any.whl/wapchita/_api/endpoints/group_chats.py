from typing import Literal, List, Optional
from datetime import datetime

import requests
from requests import Response
from requestsdantic import BaseResponse, BaseJSON
from pydantic import HttpUrl

from wapchita._api.headers import get_headers
from wapchita._api.urls import url_group_chats
from wapchita.typings import T_KindGroupChats

class LinksDetails(BaseJSON):
    details: str

class GroupDesc(BaseJSON):
    wid: str
    device: str
    communityGroups: list
    communityParentGroup: None
    createdAt: datetime
    description: Optional[str] = None
    imageUrl: Optional[HttpUrl] = None
    isArchive: bool
    isCommunityAnnounce: bool
    isPinned: bool
    isReadOnly: bool
    kind: Literal["group"]
    lastMessageAt: datetime
    lastSyncAt: datetime
    muteExpiration: None
    name: Optional[str] = None
    totalParticipants: int
    unreadCount: int
    id: str
    participants: list
    links: LinksDetails

class ResponseGroups(BaseResponse):
    data: List[GroupDesc]

    @property
    def status_code(self) -> int:
        return 200


def group_chats(
        *,
        tkn: str,
        device_id: str,
        kind: T_KindGroupChats = "any",
        page: int = 0,
        size: int = 100
) -> Response:
    """ https://app.shock.uy/docs/#tag/Groups/operation/getDeviceGroupChats"""
    url = url_group_chats(device_id=device_id)
    params = {"kind": kind, "page": page, "size": size}
    return requests.get(url=url, params=params, headers=get_headers(tkn=tkn))
