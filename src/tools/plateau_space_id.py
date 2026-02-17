"""
緯度経度から空間IDを取得するツール

"""

from mcp import types

from utils.definitions import ApiSpec

API_SPEC = ApiSpec(
    tool_name="plateau_space_id",
    target_api=None,
    allowed_params={},
)

TOOL = types.Tool(
    name=API_SPEC.tool_name,
    description="""
        このtoolは緯度経度からPLATEAU空間ID（z/f/x/y）を計算します。
        plateau_get_citygml_filesやplateau_citygml_get_featuresを実行する前に、必ずこのtoolで空間IDを取得し、
        そのIDを利用してPLATEAUのデータを取得します。
        不動産ライブラリデータの取得のみの場合はこのtoolは不要です。
        「緯度〇〇。経度〇〇の建物データください。」や「緯度〇〇。経度〇〇のPLATEAUのデータを取得してください」の場合にこのtoolが選択されます。
        PLATEAUデータを取得する前は、必ず最初にこのtoolを実行してください。
        住所や建物名が指定された場合はジオコーディングを行い、緯度経度に変換した後にこのtoolを実行してください。
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
            "z": {
                "type": "integer",
                "description": "ズームレベル（省略時18）",
                "default": 18,
            },
            "h_m": {
                "type": "number",
                "description": "標高[m]（省略時0.0）",
                "default": 0.0,
            },
        },
        "required": ["lat", "lon"],
    },
)
