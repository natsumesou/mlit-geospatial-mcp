"""
地価公示・地価調査ポイントAPIツール定義。

このモジュールは、指定した座標周辺の地価公示・地価調査データを取得するためのMCPツールを定義。

Attributes:
    API_SPEC (ApiSpec): ツールのAPI仕様
    TOOL (types.Tool): MCPツール定義
"""

from mcp import types

from utils.definitions import ApiSpec

API_SPEC = ApiSpec(
    tool_name="get_land_price_point_by_location",
    target_api=3,
    allowed_params={
        "distance",
        "year",
        "land_price_classification",
        "use_category_code",
    },
)

TOOL = types.Tool(
    name=API_SPEC.tool_name,
    description="""地価公示・地価調査のポイント（点）データを、指定した地点周辺から取得します。
                
                【概要】
                - 結果はgeojsonで返却されます。
                - 不動産情報ライブラリの「地価公示・地価調査のポイント（点）API」を呼び出すためのツールです。
                - ユーザーは「緯度・経度・距離[m]・対象年」を自然言語で指定するだけで利用できます。
                - サーバ内部では、指定した緯度・経度・距離から必要なXYZタイル（z, x, y）を計算し、APIを呼び出します。
                - 本ツールでは 425m 以内の距離のみ検索可能です（API仕様および運用ポリシーに基づく制約）。指定しない場合はデフォルトで425mが使用されます。
                
                【主な用途の例】
                - 「緯度35.681, 経度139.767周辺の地価公示データが欲しい」
                - 「この座標の半径100m以内の地価公示ポイントを一覧で教えて」
                
                【注意点】
                - distance は 425m を上限とします。これを超える値が指定された場合はエラーとして扱います。
                - XPT002 は XYZ タイル単位でデータを返すため、このツールでは distance をカバーする複数タイルを内部で取得し、
                  中心地点からの実距離でフィルタした上で返却します。
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
            "distance": {
                "type": "number",
                "description": (
                    "中心地点からの検索距離（メートル）。"
                    "この値は 0〜425[m] の範囲で指定できます。425m を超える場合はエラーになります。"
                ),
                "default": 425.0,
                "maximum": 425.0,
            },
            "year": {
                "type": "number",
                "description": (
                    "対象年（4桁の西暦）。1995〜最新年の範囲で指定可能です。"
                    "未指定の場合は 2024 年として処理します。"
                ),
            },
            "land_price_classification": {
                "type": "string",
                "description": (
                    "地価情報区分コード。\n"
                    '  "0"  : 国土交通省地価公示のみ\n'
                    '  "1"  : 都道府県地価調査のみ\n'
                    "  (未指定の場合は、地価公示＋地価調査の両方）"
                ),
                "enum": ["0", "1"],
            },
            "use_category_code": {
                "type": "string",
                "description": (
                    "用途区分コード（任意）。カンマ区切り指定可。\n"
                    '  "00": 住宅地, "03": 宅地見込地, 05: 商業地, 07: 準工業地,\n'
                    "  09: 工業地, 10: 市街地調整区域内現況宅地,\n"
                    "  13: 現況林地（公示のみ）, 20: 林地（調査のみ）,未指定：すべて"
                ),
            },
        },
        "required": ["lat", "lon"],
    },
)
