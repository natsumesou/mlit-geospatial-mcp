import contextlib
import logging
import os
from typing import Annotated

from mcp.server.fastmcp import FastMCP
from mcp.server.transport_security import TransportSecuritySettings
from starlette.applications import Starlette
from starlette.responses import JSONResponse, PlainTextResponse
from starlette.routing import Mount, Route

from request_processor.handler import handle_request
from tools import API_SPECS
from utils.payload import build_payload

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

SERVER_NAME = "mlit-geospatial-mcp"
HTTP_PATH = os.getenv("MCP_HTTP_PATH", "/mcp")


def _parse_csv_env(name: str) -> list[str]:
    value = os.getenv(name, "")
    return [item.strip() for item in value.split(",") if item.strip()]


def _build_transport_security() -> TransportSecuritySettings:
    protection_enabled = (
        os.getenv("MCP_DNS_REBINDING_PROTECTION", "false").lower() == "true"
    )
    return TransportSecuritySettings(
        enable_dns_rebinding_protection=protection_enabled,
        allowed_hosts=_parse_csv_env("MCP_ALLOWED_HOSTS"),
        allowed_origins=_parse_csv_env("MCP_ALLOWED_ORIGINS"),
    )


mcp = FastMCP(
    SERVER_NAME,
    stateless_http=True,
    json_response=True,
    transport_security=_build_transport_security(),
)


def _execute_tool(arguments: dict) -> dict:
    spec = API_SPECS["get_multi_api"]
    payload = build_payload(spec=spec, args=arguments)
    logger.info("payload: %s", payload)
    return payload


async def _process_tool(arguments: dict) -> dict:
    payload = _execute_tool(arguments)
    return await handle_request(payload)


@mcp.tool()
async def get_multi_api(
    lat: Annotated[
        float,
        "検索の中心となる地点の緯度（10進法、小数）。例: 35.681236",
    ],
    lon: Annotated[
        float,
        "検索の中心となる地点の経度（10進法、小数）。例: 139.767125",
    ],
    target_apis: Annotated[
        list[int],
        "呼び出すAPI番号。未指定または空配列の場合は全APIを取得します。",
    ],
    distance: Annotated[
        float | None,
        "中心地点からの検索距離（メートル）。0〜425[m] の範囲。",
    ] = 425.0,
    price_classification: Annotated[
        str | None,
        "価格情報区分コード。target_apiが1のとき有効。",
    ] = None,
    year: Annotated[
        int | None,
        "対象年（4桁の西暦）。target_apiが1,2,3のとき有効。",
    ] = None,
    quarter: Annotated[
        int | None,
        "取引時期（四半期）。target_apiが1のとき有効。",
    ] = None,
    language: Annotated[
        str | None,
        "出力結果の言語。target_apiが1のとき有効。",
    ] = None,
    division: Annotated[
        list[str] | None,
        "用途区分。target_apiが2のとき有効。",
    ] = None,
    land_price_classification: Annotated[
        str | None,
        "地価情報区分コード。target_apiが3のとき有効。",
    ] = None,
    use_category_code: Annotated[
        list[str] | None,
        "用途区分コード。target_apiが3のとき有効。",
    ] = None,
    administrative_area_code: Annotated[
        list[str] | None,
        "行政区域コード。target_apiが7,8,12,16,17,21,22,30のとき有効。",
    ] = None,
    welfare_facility_class_code: Annotated[
        list[str] | None,
        "福祉施設大分類コード。target_apiが12のとき有効。",
    ] = None,
    welfare_facility_middle_class_code: Annotated[
        list[str] | None,
        "福祉施設中分類コード。target_apiが12のとき有効。",
    ] = None,
    welfare_facility_minor_class_code: Annotated[
        list[str] | None,
        "福祉施設小分類コード。target_apiが12のとき有効。",
    ] = None,
    prefecture_code: Annotated[
        list[str] | None,
        "都道府県コード。target_apiが19,21,22のとき有効。",
    ] = None,
    district_code: Annotated[
        list[str] | None,
        "地区コード。target_apiが19のとき有効。",
    ] = None,
    save_file: Annotated[
        bool | None,
        "geojsonファイルを保存するかどうか。未指定時はユーザー確認扱い。",
    ] = None,
    output_dir: Annotated[
        str | None,
        "geojsonファイル保存先ディレクトリ。",
    ] = None,
) -> dict:
    """
    不動産情報ライブラリAPIを統合的に呼び出します。

    target_apis で指定した複数APIをまとめて実行し、取得結果と
    不動産情報ライブラリの地図URL、必要に応じて保存ファイルパスを返します。
    """
    arguments = {
        "lat": lat,
        "lon": lon,
        "target_apis": target_apis,
        "distance": distance,
        "price_classification": price_classification,
        "year": year,
        "quarter": quarter,
        "language": language,
        "division": division,
        "land_price_classification": land_price_classification,
        "use_category_code": use_category_code,
        "administrative_area_code": administrative_area_code,
        "welfare_facility_class_code": welfare_facility_class_code,
        "welfare_facility_middle_class_code": welfare_facility_middle_class_code,
        "welfare_facility_minor_class_code": welfare_facility_minor_class_code,
        "prefecture_code": prefecture_code,
        "district_code": district_code,
        "save_file": save_file,
        "output_dir": output_dir,
    }
    return await _process_tool(arguments)


async def healthcheck(_request):
    return JSONResponse({"status": "ok", "service": SERVER_NAME})


async def root(_request):
    return PlainTextResponse(
        f"{SERVER_NAME} is running. Streamable HTTP endpoint: {HTTP_PATH}",
        status_code=200,
    )


@contextlib.asynccontextmanager
async def lifespan(_app: Starlette):
    async with mcp.session_manager.run():
        yield


app = Starlette(
    routes=[
        Route("/", root),
        Route("/healthz", healthcheck),
        Mount("/", app=mcp.streamable_http_app()),
    ],
    lifespan=lifespan,
)


def main() -> None:
    transport = os.getenv("MCP_TRANSPORT", "stdio").lower()
    if transport == "http":
        import uvicorn

        host = os.getenv("HOST", "0.0.0.0")
        port = int(os.getenv("PORT", "8080"))
        logger.info(
            "Starting MCP server over HTTP on %s:%s (streamable=%s)",
            host,
            port,
            HTTP_PATH,
        )
        uvicorn.run(app, host=host, port=port)
        return

    logger.info("Starting MCP server over stdio")
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
