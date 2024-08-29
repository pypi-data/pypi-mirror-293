from typing import Literal

PRIORITY_DEFAULT = "normal"
Priority = Literal["low", "normal", "high", "urgent"]

SORTCHATS_DEFAULT = "date:desc"
SortChats = Literal["date:asc", "date:desc"]

T_KindGroupChats = Literal["any", "group", "community", "broadcast", "channel"]
