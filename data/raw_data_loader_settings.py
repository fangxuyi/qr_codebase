from pathlib import Path
from enum import Enum

import pandas as pd
import numpy as np
from scipy import stats

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


def money_flow_processor(pv_data):
    """pv_1min_moneyflow_standard"""

    pv_data = pv_data.sort_values("time")

    pv_data["open_time"] = pv_data["time"]
    pv_data["close_time"] = pv_data["time"]
    pv_data["prev_close"] = pv_data["pre_close"]
    pv_data["open"] = pv_data["open"]
    pv_data["high"] = pv_data["high"]
    pv_data["low"] = pv_data["low"]
    pv_data["close"] = pv_data["close"]
    pv_data["avg_turover"] = pv_data["turover"] / pv_data["dif_mi"]
    pv_data["direction"] = (pv_data["close"] / pv_data["open"] - 1).apply(np.sign)

    pv_data["ultra_large_in"] = pv_data["turover"]
    pv_data.loc[(pv_data["avg_turover"] <= 50000) | (pv_data["direction"] < 0), "ultra_large_in"] = np.nan

    pv_data["ultra_large_out"] = pv_data["turover"]
    pv_data.loc[(pv_data["avg_turover"] <= 50000) | (pv_data["direction"] > 0), "ultra_large_out"] = np.nan

    pv_data["large_in"] = pv_data["turover"]
    pv_data.loc[(pv_data["avg_turover"] <= 45000) | (pv_data["avg_turover"] > 50000) | (pv_data["direction"] < 0), "large_in"] = np.nan

    pv_data["large_out"] = pv_data["turover"]
    pv_data.loc[(pv_data["avg_turover"] <= 45000) | (pv_data["avg_turover"] > 50000) | (pv_data["direction"] > 0), "large_out"] = np.nan

    pv_data["medium_in"] = pv_data["turover"]
    pv_data.loc[(pv_data["avg_turover"] <= 40000) | (pv_data["avg_turover"] > 45000) | (pv_data["direction"] < 0), "medium_in"] = np.nan

    pv_data["medium_out"] = pv_data["turover"]
    pv_data.loc[(pv_data["avg_turover"] <= 40000) | (pv_data["avg_turover"] > 45000) | (pv_data["direction"] > 0), "medium_out"] = np.nan

    pv_data["small_in"] = pv_data["turover"]
    pv_data.loc[(pv_data["avg_turover"] > 40000) | (pv_data["direction"] < 0), "small_in"] = np.nan

    pv_data["small_out"] = pv_data["turover"]
    pv_data.loc[(pv_data["avg_turover"] > 40000) | (pv_data["direction"] > 0), "small_out"] = np.nan

    pv_data = pv_data[["code", "ultra_large_in", "ultra_large_out", "large_in", "large_out", "medium_in", "medium_out", "small_in", "small_out"]].fillna(0)

    return pv_data.groupby("code").agg({
        "ultra_large_in": sum,
        "ultra_large_out": sum,
        "large_in": sum,
        "large_out": sum,
        "medium_in": sum,
        "medium_out": sum,
        "small_in": sum,
        "small_out": sum,
    })


def intraday_liquidity_data_processor(pv_data):
    """pv_1min_liquidity"""

    pv_data = pv_data.sort_values("time")

    pv_data["open_time"] = pv_data["time"]
    pv_data["close_time"] = pv_data["time"]
    pv_data["prev_close"] = pv_data["pre_close"]
    pv_data["open"] = pv_data["open"]
    pv_data["high"] = pv_data["high"]
    pv_data["low"] = pv_data["low"]
    pv_data["close"] = pv_data["close"]
    pv_data["open_volume"] = pv_data["volume"]
    pv_data["close_volume"] = pv_data["volume"]
    pv_data["max_volume"] = pv_data["volume"]
    pv_data["up_volume"] = pv_data["volume"]
    pv_data["down_volume"] = pv_data["volume"]
    pv_data["min_volume"] = pv_data["volume"].replace(0., np.nan)
    pv_data["minute_return"] = pv_data["close"] / pv_data["open"] - 1

    minute_return_mask_up = pv_data["minute_return"].apply(lambda x: x > 0).values
    minute_return_mask_down = pv_data["minute_return"].apply(lambda x: x < 0).values
    pv_data.loc[minute_return_mask_down, "up_volume"] = 0
    pv_data.loc[minute_return_mask_up, "down_volume"] = 0

    pv_data["turnover_high_low"] = (pv_data["high"] - pv_data["low"]) / pv_data["turover"]
    pv_data["turnover_high_open"] = (pv_data["high"] - pv_data["open"]) / pv_data["turover"]

    return pv_data.groupby("code").agg({
        "open_time": min,
        "close_time": max,
        "prev_close": "first",
        "open": "first",
        "high": max,
        "low": min,
        "close": "last",
        "open_volume": "first",
        "close_volume": "last",
        "max_volume": max,
        "min_volume": min,
        "up_volume": sum,
        "down_volume": sum,
        "turnover_high_low": "mean",
        "turnover_high_open": "mean",
    })

def intraday_volatility(pv_data):
    """pv_1min_intraday_volatility"""

    def std(x):
        return np.std(x.dropna())

    pv_data = pv_data.sort_values("time")

    pv_data["open"] = pv_data["open"]
    pv_data["close"] = pv_data["close"]

    pv_data["intraday_vol"] = pv_data["close"] / pv_data["open"] - 1
    pv_data["intraday_vol_up"] = pv_data["intraday_vol"].apply(lambda x: x if x > 0 else np.nan)
    pv_data["intraday_vol_down"] = pv_data["intraday_vol"].apply(lambda x: x if x < 0 else np.nan)
    pv_data["intraday_return_up"] = pv_data["intraday_vol"].apply(lambda x: x if x > 0 else np.nan)
    pv_data["intraday_return_down"] = pv_data["intraday_vol"].apply(lambda x: x if x < 0 else np.nan)

    return pv_data.groupby("code").agg({
        "open": "first",
        "close": "last",
        "intraday_vol": std,
        "intraday_vol_up": std,
        "intraday_vol_down": std,
        "intraday_return_up": "sum",
        "intraday_return_down": "sum",
    })


def daily_vwap(pv_data):
    """pv_1min_daily_vwap"""

    pv_data = pv_data.sort_values("time")

    pv_data["open"] = pv_data["open"]
    pv_data["close"] = pv_data["close"]
    pv_data["return"] = pv_data["close"] / pv_data["open"] - 1

    pv_data["volume"] = pv_data["volume"]
    pv_data["vwap"] = pv_data["accturover"] / pv_data["accvolume"]
    pv_data["weighted_return"] = pv_data["return"] * pv_data["volume"]

    pv_data = pv_data.groupby("code").agg({
        "vwap": "last",
        "weighted_return": "sum",
        "volume": "sum",
    })
    pv_data["weighted_avg_return"] = pv_data["weighted_return"] / pv_data["volume"]
    return pv_data


def daily_return_driven_by_turnover(pv_data):
    """pv_1min_daily_turnover"""

    pv_data = pv_data.sort_values("time")

    pv_data["open"] = pv_data["open"]
    pv_data["close"] = pv_data["close"]
    pv_data["return"] = (pv_data["close"] / pv_data["open"] - 1).apply(abs)
    pv_data["return_up"] = (pv_data["close"] / pv_data["open"] - 1).apply(lambda x: x if x > 0 else np.nan)
    pv_data["return_down"] = (pv_data["close"] / pv_data["open"] - 1).apply(lambda x: x if x < 0 else np.nan)

    pv_data["turover"] = pv_data["turover"]
    pv_data["abs_return_turnover"] = pv_data["return"] * 10 ** (10) / pv_data["turover"]
    pv_data["up_return_turnover"] = pv_data["return_up"] * 10 ** (10) / pv_data["turover"]
    pv_data["down_return_turnover"] = pv_data["return_down"] * 10 ** (10) / pv_data["turover"]

    pv_data = pv_data.groupby("code").agg({
        "abs_return_turnover": "mean",
        "up_return_turnover": "mean",
        "down_return_turnover": "mean",
    })
    return pv_data


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
        "high_low_diff": "sum",
        "open": "first",
        "close": "last"
    })


def minute_open_high_low_close_with_volume(pv_data):
    """pv_1min_high_low_open_close_with_volume_ratio"""

    pv_data = pv_data.sort_values("time")

    pv_data["open_time"] = pv_data["time"]
    pv_data["close_time"] = pv_data["time"]
    pv_data["prev_close"] = pv_data["pre_close"]
    pv_data["open"] = pv_data["open"]
    pv_data["high"] = pv_data["high"]
    pv_data["low"] = pv_data["low"]
    pv_data["close"] = pv_data["close"]
    pv_data["volume"] = pv_data.apply(
        lambda x: x["volume"] if abs(x["close"] - x["open"]) <= 0.5 * abs(x["high"] - x["low"]) else 0, axis=1)

    return pv_data.groupby("code").agg({
        "high": max,
        "low": min,
        "volume": "sum",
        "open": "first",
        "close": "last"
    })


def intraday_pvi_nvi(pv_data):
    """pv_1min_intraday_pvi_nvi"""

    pv_data = pv_data.sort_values("time")

    pv_data["open_time"] = pv_data["time"]
    pv_data["close_time"] = pv_data["time"]
    pv_data["prev_close"] = pv_data["pre_close"]
    pv_data["open"] = pv_data["open"]
    pv_data["high"] = pv_data["high"]
    pv_data["low"] = pv_data["low"]
    pv_data["close"] = pv_data["close"]
    pv_data["volume"] = pv_data["volume"]
    pv_data["return"] = pv_data["close"] / pv_data["open"] - 1

    pv_data_volume = pv_data.pivot_table(index="time", columns="code", values="volume").fillna(0)
    pv_data_volume = pv_data_volume.diff()

    pv_data_return = pv_data.pivot_table(index="time", columns="code", values="return").fillna(0)
    pv_data_return_upside = pv_data_return[pv_data_volume > 0].sum().rename("up_volume_return")
    pv_data_return_downside = pv_data_return[pv_data_volume < 0].sum().rename("down_volume_return")

    return pd.concat([pv_data_return_upside, pv_data_return_downside], axis=1)


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


def momentum_without_extreme_value(pv_data):
    """pv_1min_daily_return_without_extreme_value"""

    pv_data["return"] = pv_data["close"] / pv_data["open"] - 1
    pv_data = pv_data.pivot_table(index="time", columns="code", values="return")

    for col in pv_data:
        pv_data.loc[(np.abs(stats.zscore(pv_data[col])) > 3), col] = 0.

    return pd.DataFrame(pv_data.sum().transpose().rename("returns"))


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
