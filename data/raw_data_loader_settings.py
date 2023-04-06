from pathlib import Path
from enum import Enum


version = "pv_1min_standard"


BASE_DIR = str(Path(__file__).resolve().parent.parent)
DataPath = BASE_DIR + r"\Data"
ReferenceDataPath = DataPath + r"\other"
PVDataPath = DataPath
OutputDataPath = DataPath + r"\processed"
WARNING_LOGFILE = r"logging\warning_logging_{}.txt"
AlphaOutputPath = DataPath + r"\alpha"
PerformanceOutputPath = DataPath + r"\performance"
TearSheetOutputPath = DataPath + r"\tearsheet"


def standard_pv_data_processor(pv_data):
    pv_data = pv_data.sort_values("time")

    pv_data["open_time"] = pv_data["time"]
    pv_data["close_time"] = pv_data["time"]
    pv_data["prev_close"] = pv_data["pre_close"]
    pv_data["open"] = pv_data["open"]
    pv_data["high"] = pv_data["high"]
    pv_data["low"] = pv_data["low"]
    pv_data["close"] = pv_data["close"]
    pv_data["daily_volume"] = pv_data["accvolume"]
    pv_data["daily_turover"] = pv_data["accturover"]
    pv_data["daily_tradenum"] = pv_data["match_items"]

    return pv_data.groupby("code").agg({
        "open_time": min,
        "close_time": max,
        "prev_close": "first",
        "open": "first",
        "high": max,
        "low": min,
        "close": "last",
        "daily_volume": "last",
        "daily_turover": "last",
        "daily_tradenum": "last",
    })


class FileOrgStructure(Enum):
    DATECOLUMN = 1


"""Directory saved in tuple (dir, filepattern)"""
ReferenceData = {
    # Dates
    "CumulativeAdjustmentFactor": (r"\adj_fct", r"\yyyy\yyyymmdd.csv"),
    "HaltDate": (r"\date", r"\halt_date.csv"),
    "ListDelistDate": (r"\date", r"\lst_date.csv"),
    "STDate": (r"\date", r"\st_date.csv"),
    "Calendar": (r"\date", r"\trd_date.csv"),
    # Index Performance
    "IndexPerformance": (r"\idx", r"\yyyy\yyyymmdd.csv"),
    # Limit Up and Limit Down Prices
    "LimitPrices": (r"\lmt", r"\yyyy\yyyymmdd.csv"),
    # MarketValue
    "MarketValue": (r"\mkt_val", r"\yyyy\yyyymmdd.csv"),
    # Sector Classification
    "Sector": (r"\sw", r"\yyyy\yyyymmdd.csv"),
    # Index Universe
    "HS300": (r"\univ\hs300", r"\yyyy\yyyymmdd.csv"),
    "ZZ500": (r"\univ\zz500", r"\yyyy\yyyymmdd.csv"),
    "ZZ800": (r"\univ\zz800", r"\yyyy\yyyymmdd.csv"),
    "ZZ1000": (r"\univ\zz1000", r"\yyyy\yyyymmdd.csv"),
    "ZZ9999": (r"\univ\zz9999", r"\yyyy\yyyymmdd.csv"),
}

PriceData = {
    "1min_PV": (r"\qishi_1min_zip", r"\yyyymmdd\stockid.csv")
}

PriceDataColumns = ["code", "date", "time", "pre_close",
                    "open", "high", "low", "close",
                    "volume", "turnover", "dif_mi",
                    "accvolume", "accturover", "match_items"]
