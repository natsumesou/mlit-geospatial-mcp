"""
都市計画区域・区域区分APIツール定義。

このモジュールは、指定した座標に基づき都市計画区域・区域区分データを取得するためのMCPツールを定義。

Attributes:
    API_SPEC (ApiSpec): ツールのAPI仕様
    TOOL (types.Tool): MCPツール定義
"""

from mcp import types

from utils.definitions import ApiSpec

API_SPEC = ApiSpec(
    tool_name="get_urban_planning",
    target_api=4,
    allowed_params=set(),
)

TOOL = types.Tool(
    name=API_SPEC.tool_name,
    description="""都市計画区域・区域区分データを取得します。
                
                【概要】
                - 結果はgeojsonで返却します。
                - 不動産情報ライブラリの「都市計画区域・区域区分API」を呼び出すためのツールです。
                - ユーザーは「緯度・経度」を自然言語で指定するだけで利用できます。
                - サーバ内部では、指定した緯度・経度・距離から必要なXYZタイル（z, x, y）を計算し、APIを呼び出します。
                - 本ツールでは 検索座標（緯度経度）と重なるポリゴンのみ結果を返します。
                
                【主な用途の例】
                - 「緯度35.681, 経度139.767の都市計画区域・区域区分データが欲しい」
                
                【注意点】
                - XKT001 は ポリゴンデータが返却されますが、検索座標と重なる結果がない場合は、「結果なし」となります。
                """.strip(),
    inputSchema={
        "type": "object",
        "properties": {
            "lat": {
                "type": "number",
                "description": "検索の中心となる地点の緯度（10進法、小数）。例: 35.681236",
            },
            "lon": {
                "type": "number",
                "description": "検索の中心となる地点の経度（10進法、小数）。例: 139.767125",
            },
        },
        "required": ["lat", "lon"],
    },
)
