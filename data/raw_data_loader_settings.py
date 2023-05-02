from pathlib import Path
from enum import Enum

import pandas as pd
import numpy as np

BASE_DIR = str(Path(__file__).resolve().parent.parent.parent)
DataPath = BASE_DIR + r"\Data"
ReferenceDataPath = DataPath + r"\other"
PVDataPath = DataPath
OutputDataPath = DataPath + r"\processed"
WARNING_LOGFILE = r"logging\warning_logging_{}.txt"
AlphaOutputPath = DataPath + r"\alpha"
PerformanceOutputPath = DataPath + r"\performance"
TearSheetOutputPath = DataPath + r"\tearsheet"
OtherPerfOutputPath = DataPath + r"\othermetrics"


def standard_pv_data_processor(pv_data):
    """pv_1min_standard"""

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


def minute_open_high_low_close(pv_data):
    """pv_1min_high_low_open_close"""

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

    pv_data["high_low_diff"] = pv_data["high"] - pv_data["low"]

    return pv_data.groupby("code").agg({
        "high": max,
        "low": min,
        "high_low_diff": "sum"
    })


def big_small_turnover_direction(pv_data):
    """pv_1min_large_small_turnovers"""

    pv_data["return"] = pv_data["close"] / pv_data["open"] - 1
    pv_data_turnover = pv_data.pivot_table(index="time", columns="code", values="turover").replace(0., np.nan)
    largest_mins_per_code = {}
    smallest_mins_per_code = {}
    for col in pv_data_turnover:
        largest_mins_per_code[col] = list(pv_data_turnover[col].nlargest(20).index)
        smallest_mins_per_code[col] = list(pv_data_turnover[col].nsmallest(20).index)

    largest_turnover_per_code = []
    smallest_turnover_per_code = []
    largest_returns_per_code = []
    smallest_returns_per_code = []
    diff_returns_per_code = []
    pv_data_return = pv_data.pivot_table(index="time", columns="code", values="return")
    pv_data_return = pv_data_return.reindex(pv_data_turnover.columns, axis=1)
    pv_data_return = pv_data_return.reindex(pv_data_turnover.index, axis=0)
    for col in pv_data_return:
        largest_returns = pv_data_return.loc[largest_mins_per_code[col], col]
        largest_turnovers = pv_data_turnover.loc[largest_mins_per_code[col], col]
        largest_weighted_returns = (largest_returns * largest_turnovers).sum() / largest_turnovers.sum()
        largest_returns_per_code.append((col, largest_weighted_returns))
        largest_turnover_per_code.append((col, largest_turnovers.sum()))

        smallest_returns = pv_data_return.loc[smallest_mins_per_code[col], col]
        smallest_turnovers = pv_data_turnover.loc[smallest_mins_per_code[col], col]
        smallest_weighted_returns = (smallest_returns * smallest_turnovers).sum() / smallest_turnovers.sum()
        smallest_returns_per_code.append((col, smallest_weighted_returns))
        smallest_turnover_per_code.append((col, smallest_turnovers.sum()))

        diff_returns_per_code.append((col, largest_weighted_returns - smallest_weighted_returns))

    largest_returns_per_code_df = pd.DataFrame(largest_returns_per_code)
    smallest_returns_per_code_df = pd.DataFrame(smallest_returns_per_code)
    diff_returns_per_code_df = pd.DataFrame(diff_returns_per_code)
    largest_turnover_per_code_df = pd.DataFrame(largest_turnover_per_code)
    smallest_turnover_per_code_df = pd.DataFrame(smallest_turnover_per_code)

    largest_returns_per_code_df.columns = ["code", "biggest_turnover_returuns"]
    smallest_returns_per_code_df.columns = ["code", "smallest_turnover_returns"]
    diff_returns_per_code_df.columns = ["code", "diff_return"]
    largest_turnover_per_code_df.columns = ["code", "biggest_turnover_sum"]
    smallest_turnover_per_code_df.columns = ["code", "smallest_turnover_sum"]

    largest_returns_per_code_df = largest_returns_per_code_df.set_index("code")
    smallest_returns_per_code_df = smallest_returns_per_code_df.set_index("code")
    diff_returns_per_code_df = diff_returns_per_code_df.set_index("code")
    largest_turnover_per_code_df = largest_turnover_per_code_df.set_index("code")
    smallest_turnover_per_code_df = smallest_turnover_per_code_df.set_index("code")

    return pd.concat([largest_returns_per_code_df, smallest_returns_per_code_df, diff_returns_per_code_df,
                      largest_turnover_per_code_df, smallest_turnover_per_code_df], axis=1)


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
