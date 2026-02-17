"""
地図表示URL生成ロジック
lat, lon, target_apis から地図表示用URLを生成する
"""

from utils.const import MAP_URL_ZOOM, SURVER_YEAR

# target_api番号 → レイヤ・条件・追加パラメータ対応表
API_LAYERS = {
    3: [
        {
            "layer": "publicNotices",
            "condition": lambda p: (
                p.get("land_price_classification") in (None, "0")
                and (
                    not p.get("use_category_code")
                    or any(
                        code.strip() in LAYER_PARAMS["publicNotices"]
                        for code in p.get("use_category_code", [])
                        if code.strip()
                    )
                )
            ),
            "params": lambda p: (
                [
                    f"publicNotices={c.strip()}"
                    for c in p.get("use_category_code", [])
                    if c.strip()
                ]
                if p.get("use_category_code")
                else [f"publicNotices={v}" for v in LAYER_PARAMS["publicNotices"]]
            ),
        },
        {
            "layer": "surveys",
            "condition": lambda p: (
                p.get("land_price_classification") in (None, "1")
                and (
                    not p.get("use_category_code")
                    or any(
                        code.strip() in LAYER_PARAMS["publicNotices"]
                        for code in p.get("use_category_code", [])
                        if code.strip()
                    )
                )
            ),
            "params": lambda p: (
                [
                    f"publicNotices={c.strip()}"
                    for c in p.get("use_category_code", [])
                    if c.strip()
                ]
                if p.get("use_category_code")
                else [f"publicNotices={v}" for v in LAYER_PARAMS["publicNotices"]]
            ),
        },
    ],
    12: [
        # 常にwelfareFacilityレイヤを追加
        {
            "layer": "welfareFacility",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
        # 各分類ごと
        {
            "layer": "shelterLayer",
            "condition": lambda p: "01"
            in [
                c.strip() for c in p.get("welfare_facility_class_code", []) if c.strip()
            ],
            "params": lambda p: [],
        },
        {
            "layer": "elderlyWelfareFacilityLayer",
            "condition": lambda p: "02"
            in [
                c.strip() for c in p.get("welfare_facility_class_code", []) if c.strip()
            ],
            "params": lambda p: [],
        },
        {
            "layer": "facilityForTheHandicappedLayer",
            "condition": lambda p: "03"
            in [
                c.strip() for c in p.get("welfare_facility_class_code", []) if c.strip()
            ],
            "params": lambda p: [],
        },
        {
            "layer": "socialParticipationSupportFacilitiesLayer",
            "condition": lambda p: "04"
            in [
                c.strip() for c in p.get("welfare_facility_class_code", []) if c.strip()
            ],
            "params": lambda p: [],
        },
        {
            "layer": "childWelfareFacilityLayer",
            "condition": lambda p: "05"
            in [
                c.strip() for c in p.get("welfare_facility_class_code", []) if c.strip()
            ],
            "params": lambda p: [],
        },
        {
            "layer": "maternalAndChildWelfareLayer",
            "condition": lambda p: "06"
            in [
                c.strip() for c in p.get("welfare_facility_class_code", []) if c.strip()
            ],
            "params": lambda p: [],
        },
        {
            "layer": "otherWelfareFacilityLayer",
            "condition": lambda p: "99"
            in [
                c.strip() for c in p.get("welfare_facility_class_code", []) if c.strip()
            ],
            "params": lambda p: [],
        },
        # その他はデフォルト
        *[
            {
                "layer": l,
                "condition": lambda p, l=l: not any(
                    code.strip() == l_code
                    for code in p.get("welfare_facility_class_code", [])
                    if code.strip()
                    for l_code in ["01", "02", "03", "04", "05", "06", "99"]
                    if l
                    == {
                        "shelterLayer": "01",
                        "elderlyWelfareFacilityLayer": "02",
                        "facilityForTheHandicappedLayer": "03",
                        "socialParticipationSupportFacilitiesLayer": "04",
                        "childWelfareFacilityLayer": "05",
                        "maternalAndChildWelfareLayer": "06",
                        "otherWelfareFacilityLayer": "99",
                    }[l]
                ),
                "params": lambda p: [],
            }
            for l in [
                "shelterLayer",
                "elderlyWelfareFacilityLayer",
                "facilityForTheHandicappedLayer",
                "socialParticipationSupportFacilitiesLayer",
                "childWelfareFacilityLayer",
                "maternalAndChildWelfareLayer",
                "otherWelfareFacilityLayer",
            ]
        ],
    ],
    # 他APIは従来通りレイヤ名のみ
    4: [
        {"layer": l, "condition": lambda p, l=l: True, "params": lambda p: []}
        for l in [
            "urbanPlanAreaLayer",
            "areaClassification",
            "urbanizationPromotionAreaLayer",
            "urbanizationControlAreaLayer",
        ]
    ],
    5: [
        {
            "layer": "useAreaLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    6: [
        {
            "layer": "locationOptimizePlanAreaLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    7: [
        {
            "layer": "elementarySchoolAreaLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    8: [
        {
            "layer": "juniorHighSchoolAreaLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    9: [
        {"layer": l, "condition": lambda p, l=l: True, "params": lambda p: []}
        for l in [
            "school",
            "elementarySchoolLayer",
            "juniorHighSchoolLayer",
            "secondarySchoolLayer",
            "highSchoolLayer",
            "technicalSchoolLayer",
            "juniorCollegeLayer",
            "universityLayer",
            "specialSupportSchoolLayer",
            "compulsoryEducationSchoolLayer",
            "miscellaneousSchoolLayer",
            "professionalTrainingCollegeLayer",
        ]
    ],
    10: [
        {
            "layer": "preschoolLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    11: [
        {"layer": l, "condition": lambda p, l=l: True, "params": lambda p: []}
        for l in [
            "medicalInstitution",
            "hospitalLayer",
            "clinicLayer",
            "dentalClinicLayer",
        ]
    ],
    14: [
        {
            "layer": "fireProtectionAreaLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    15: [
        {
            "layer": "passengersByStationLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    16: [
        {
            "layer": "disasterRiskAreaLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    17: [
        {
            "layer": "culturalFacilityLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    18: [
        {"layer": l, "condition": lambda p, l=l: True, "params": lambda p: []}
        for l in [
            "cityTownHall",
            "townHallLayer",
            "townHallBranchLayer",
            "otherAdministrativeServicesLayer",
            "publicHallLayer",
            "meetingFacilityLayer",
        ]
    ],
    19: [
        {
            "layer": "naturalParkAreaLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    20: [
        {
            "layer": "developedLandLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    21: [
        {
            "layer": "landslidePreventionLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    22: [
        {
            "layer": "collapseRiskAreaLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    23: [
        {
            "layer": "districtPlanLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    24: [
        {
            "layer": "advancedUseLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
    25: [
        {
            "layer": "liqueFactionLayer",
            "condition": lambda p: True,
            "params": lambda p: [],
        },
    ],
}

# レイヤ個別パラメータ（例：地価公示の用途区分）
LAYER_PARAMS = {
    "publicNotices": ["00", "03", "05", "07", "09", "10", "13", "20"],
}


# --- 地図表示URL生成 ---
def build_map_url(
    lat: float, lon: float, target_apis: list[int], params: dict = None
) -> str:
    """
    地図表示URLを生成する（API_LAYERSの条件・パラメータ対応で分岐レス）

    1. API3ならsurveyYearを追加
    2. API_LAYERSの各レイヤ条件関数でTrueになったものだけ追加
    3. 追加パラメータ関数で返された値もURLに追加
    4. 座標・ズーム値（API3かつyear指定ならyear、なければデフォルト）を追加
    5. すべてのパラメータを&区切りでURLにして返す
    """
    base_url = "https://www.reinfolib.mlit.go.jp/map?"
    url_params: list[str] = []
    params = params or {}

    # API 3: surveyYearはparams["year"]があればそれを、なければSURVER_YEAR
    if 3 in target_apis:
        year = params.get("year")
        if isinstance(year, int) or (isinstance(year, float) and year.is_integer()):
            url_params.append(f"surveyYear={int(year)}")
        else:
            url_params.append(f"surveyYear={SURVER_YEAR}")

    for api in target_apis:
        for entry in API_LAYERS.get(api, []):
            if entry["condition"](params):
                url_params.append(f"layers={entry['layer']}")
                for v in entry["params"](params):
                    url_params.append(v)

    # 座標・ズーム（zoomは常にMAP_URL_ZOOM固定）
    url_params.append(f"x={lat}")
    url_params.append(f"y={lon}")
    url_params.append(f"zoom={MAP_URL_ZOOM}")

    return base_url + "&".join(url_params)
