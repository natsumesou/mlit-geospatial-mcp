# APIの定義

from dataclasses import dataclass
from typing import Set


@dataclass(frozen=True)
class ApiSpec:
    """
    API仕様を定義するデータクラス。

    Attributes:
        tool_name : tool名
        target_api: 単一API指定（multi_api時は None）
        allowed_params: 指定可能なパラメータ
    """

    tool_name: str
    target_api: int
    allowed_params: Set[str]
