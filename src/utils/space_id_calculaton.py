"""
PLATEAU 空間ID 変換ユーティリティ
- 水平(x,y)：Slippy Map (Web Mercator, XYZ) と同一
- 鉛直(f)：H=2^25[m] を用いた高さ帯 f = floor( (2^z) * h / H )
- 仕様出典：
  - 4次元時空間情報利活用のための空間IDガイドライン（1.0版） ・・・ fの定義/H=2^25、水平方向はXYZと同一  [IPA/経産省ほか]
  - 実装解説記事（式の明示） ・・・ f, x, y の各式
  - Slippy Map (XYZ) の公式式 ・・・ x, y の計算、緯度クリップ、floor
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from typing import Tuple

# --- 定数（仕様どおり） ---
WEB_MERCATOR_LAT_MAX = 85.05112878  # 有効緯度の上限（±85.05112878°）  [Slippy Map仕様]
Z_HEIGHT_EXP = 25  # H = 2^25 [m]                         [空間ID仕様]
H_METERS = 2**Z_HEIGHT_EXP  # 33,554,432 m


@dataclass(frozen=True)
class SpatialID:
    """
    PLATEAU空間ID (z/f/x/y) を表現するデータクラス。
    """

    z: int
    f: int
    x: int
    y: int

    def as_string(self) -> str:
        """
        空間IDを 'z/f/x/y' 形式の文字列で返す。
        Returns:
            str: 'z/f/x/y' 形式の空間ID文字列
        """
        return f"{self.z}/{self.f}/{self.x}/{self.y}"


def _clip_lat(lat_deg: float) -> float:
    """
    Web Mercator の有効範囲に緯度をクリップ（±85.05112878°）。

    Args:
        lat_deg (float): 緯度（度）
    Returns:
        float: クリップ後の緯度
    """
    return max(min(lat_deg, WEB_MERCATOR_LAT_MAX), -WEB_MERCATOR_LAT_MAX)


def lonlat_to_xyz(lon_deg: float, lat_deg: float, z: int) -> Tuple[int, int]:
    """
    WGS84/JGD2024 の (lon,lat) とズーム z から XYZ タイル座標 (x, y) を返す。

    Args:
        lon_deg (float): 経度（度）
        lat_deg (float): 緯度（度）
        z (int): ズームレベル
    Returns:
        tuple[int, int]: (x, y) タイル座標
    """
    lat_deg = _clip_lat(lat_deg)
    n = 2**z

    # 経度→x
    x_float = n * ((lon_deg + 180.0) / 360.0)
    x = math.floor(x_float)

    # 緯度→y（Web Mercator）
    lat_rad = math.radians(lat_deg)
    y_float = (
        n
        * (1.0 - (math.log(math.tan(lat_rad) + (1.0 / math.cos(lat_rad))) / math.pi))
        / 2.0
    )
    y = math.floor(y_float)

    return x, y


def elevation_to_f(h_m: float, z: int) -> int:
    """
    標高 h[m] とズーム z から f（高さ帯インデックス）を返す。

    Args:
        h_m (float): 標高[m]
        z (int): ズームレベル
    Returns:
        int: 高さ帯インデックス f
    """
    n = 2**z
    return math.floor(n * h_m / H_METERS)


def spatial_id_from_wgs84(
    lat_deg: float, lon_deg: float, z: int = 18, h_m: float = 0.0
) -> SpatialID:
    """
    入力（lat[°], lon[°], z, h[m]）から PLATEAU 空間ID (z/f/x/y) を返す。

    Args:
        lat_deg (float): 緯度（度）
        lon_deg (float): 経度（度）
        z (int, optional): ズームレベル（既定18）
        h_m (float, optional): 標高[m]（既定0.0）
    Returns:
        SpatialID: 空間IDデータクラス
    """
    x, y = lonlat_to_xyz(lon_deg, lat_deg, z)
    f = elevation_to_f(h_m, z)
    return SpatialID(z=z, f=f, x=x, y=y)
