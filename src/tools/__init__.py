"""
MCPツールの初期化モジュール。

このモジュールでは、各ツールのAPI仕様とツール定義をインポートし、
MCPに登録するためのリストと辞書を提供。

Attributes:
    TOOLS (list): MCPに登録するツールのリスト。
    API_SPECS (dict): ツール名をキーとしたAPI仕様の辞書。
"""

from tools.land_price_point_by_location import API_SPEC as LAND_PRICE_SPEC
from tools.land_price_point_by_location import TOOL as LAND_PRICE_TOOL
from tools.multi_api import API_SPEC as MULTI_API_SPEC
from tools.multi_api import TOOL as MULTI_API_TOOL
from tools.plateau_space_id import API_SPEC as PLATEAU_SPACE_ID_SPEC
from tools.plateau_space_id import TOOL as PLATEAU_SPACE_ID_TOOL
from tools.urban_planning import API_SPEC as URBAN_PLANNING_SPEC
from tools.urban_planning import TOOL as URBAN_PLANNING_TOOL
from tools.zoning_district import API_SPEC as ZONING_DISTRICT_SPEC
from tools.zoning_district import TOOL as ZONING_DISTRICT_TOOL

# MCPに登録するツール一覧
TOOLS = [
    LAND_PRICE_TOOL,
    URBAN_PLANNING_TOOL,
    ZONING_DISTRICT_TOOL,
    MULTI_API_TOOL,
    PLATEAU_SPACE_ID_TOOL,
]

# tool_name→ApiSpecの辞書
API_SPECS = {
    LAND_PRICE_SPEC.tool_name: LAND_PRICE_SPEC,
    URBAN_PLANNING_SPEC.tool_name: URBAN_PLANNING_SPEC,
    ZONING_DISTRICT_SPEC.tool_name: ZONING_DISTRICT_SPEC,
    MULTI_API_SPEC.tool_name: MULTI_API_SPEC,
    PLATEAU_SPACE_ID_SPEC.tool_name: PLATEAU_SPACE_ID_SPEC,
}
