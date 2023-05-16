import numpy as np

from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
import pandas as pd


class Momentum:

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = (returns + 1).prod() - 1
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class Reversal:

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = (returns + 1).prod() - 1
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = - (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class GappedReversal:

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookbackend"]:idx -
                                                                                                                  self.parameter[
                                                                                                                      "lookbackstart"] + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = (returns + 1).prod() - 1
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = - (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class TimeSeriesMomentum:

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            return_diffs = returns.tail(1) - returns.mean()
            total_return_avg = return_diffs.mean()
            total_return_sum = return_diffs.apply(lambda x: abs(x)).sum() / 2
            weight = (return_diffs - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class MomentumChange:

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[
                                                                  idx - self.parameter["lookback"] - self.parameter[
                                                                      "gap"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            momentum_change = ((returns + 1).tail(self.parameter["lookback"]).prod() - 1) - (
                        (returns + 1).head(self.parameter["lookback"]).prod() - 1)
            total_return_avg = momentum_change.mean()
            total_return_sum = momentum_change.apply(lambda x: abs(x)).sum() / 2
            weight = (momentum_change - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class MaxRatio:

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)
            mocked_prices = (returns + 1).cumprod()

            max_ratio = mocked_prices.tail(1) - mocked_prices.max()
            total_return_avg = max_ratio.mean()
            total_return_sum = max_ratio.apply(lambda x: abs(x)).sum() / 2
            weight = (max_ratio - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class BinaryCount:

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            binary_count = returns.applymap(np.sign).sum()
            total_return_avg = binary_count.mean()
            total_return_sum = binary_count.apply(lambda x: abs(x)).sum() / 2
            weight = (binary_count - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class VolAdjMomentum:

    """large return should be more significant for low vol period: continuously moving up is more valuable"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[
                                                                  idx - self.parameter["volwindow"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            vol_adj_return = returns.tail(self.parameter["lookbackwindow"]).mean() / returns.std()
            total_return_avg = vol_adj_return.mean()
            total_return_sum = vol_adj_return.apply(lambda x: abs(x)).sum() / 2
            weight = (vol_adj_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class VolAdjTSMomentum:

    """time series variation adjusted by volatility: change in low vol period is more valuable"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[
                                                                  idx - self.parameter["volwindow"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            vol_adj_return = (returns.tail(self.parameter["lookbackwindow"]).mean() - returns.mean()) / returns.std()
            total_return_avg = vol_adj_return.mean()
            total_return_sum = vol_adj_return.apply(lambda x: abs(x)).sum() / 2
            weight = (vol_adj_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class EWMAAdjMomentum:

    """recent price action is more valuable"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookbackwindow"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            ewma_adj_return = returns.ewm(span=self.parameter["span"]).mean().tail(1).transpose()[str(date)]
            total_return_avg = ewma_adj_return.mean()
            total_return_sum = ewma_adj_return.apply(lambda x: abs(x)).sum() / 2
            weight = (ewma_adj_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class ExpandedTimeSeriesMomentum:

    """smooth out recent price movement noise"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            return_diffs = returns.tail(self.parameter["shortwindow"]).mean() - returns.mean()
            total_return_avg = return_diffs.mean()
            total_return_sum = return_diffs.apply(lambda x: abs(x)).sum() / 2
            weight = (return_diffs - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class OpenToCloseMomentum:

    """open to close should have better trending than close to close"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["open", "close", "code"]) #no cum_adjf for intraday
            returns = returns.replace(0.,np.nan)
            returns["return"] = returns["close"] / returns["open"] - 1
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = (returns + 1).prod() - 1
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class OpenToCloseMomentumWithVolumeFilter:

    """decreasing volume generates higher momentum?"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            volumes = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["daily_volume", "code"])
            volumes["code"] = volumes["code"].apply(lambda x: x.decode('utf-8'))
            volumes = volumes.pivot_table(index="date", columns="code", values="daily_volume")
            volumes = volumes.reindex(universe, axis=1).dropna(how="any", axis=1)
            volumes_change = (volumes.diff() / volumes.shift()).mean()

            total_return = (returns + 1).prod() - 1
            total_return = total_return[volumes_change < 0]
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class OpenToCloseMomentumWithVolumeCorr:

    """same direction movement in volume and price is bearish?"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            volumes = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["daily_volume", "code"])
            volumes["code"] = volumes["code"].apply(lambda x: x.decode('utf-8'))
            volumes = volumes.pivot_table(index="date", columns="code", values="daily_volume")
            volumes = volumes.reindex(universe, axis=1).dropna(how="any", axis=1)
            volumes_change = volumes.diff() / volumes.shift()

            ranked_returns = returns.rank(axis=0)
            ranked_volumes_change = volumes_change.rank(axis=0)
            corr = ranked_returns.corrwith(ranked_volumes_change, axis=0)
            corr = corr.dropna()

            corr_avg = corr.mean()
            corr_sum = corr.apply(lambda x: abs(x)).sum() / 2
            weight = - (corr - corr_avg) / corr_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class OpenToCloseReversal:

    """this is only here because it worked empirically"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["open", "close", "code"]) #no cum_adjf for intraday
            returns = returns.replace(0.,np.nan)
            returns["return"] = returns["close"] / returns["open"] - 1
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = (returns + 1).prod() - 1
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = - (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class ConsistencyInIntradayPriceMovement:

    """gradual price movement might indicate a stronger trend"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_high_low_open_close",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["open", "close", "high_low_diff", "code"])
            returns["ratio"] = (returns["close"] - returns["open"]) / returns["high_low_diff"]
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="ratio")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = returns.mean()
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = - (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class VolumeConsistency:

    """minute level price movement consistency weighted by volume"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_high_low_open_close_with_volume_ratio",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["volume", "code"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="volume")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = returns.mean()
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = - (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class TopBottomTradeReversal:

    """if largest trade and smallest trades are correspond to opposite price movement, top returns tend to be fake"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_large_small_turnovers",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["code", "diff_return"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="diff_return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = returns.mean()
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = - (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class ShortTermLowReversal:

    """minimum of low price over a few period of time. the lower the bigger chance of reversal"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["code", "open"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="open")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            returns_ranked = returns.rank(axis=1).rank(axis=0).tail(1).mean()
            total_return_avg = returns_ranked.mean()
            total_return_sum = returns_ranked.apply(lambda x: abs(x)).sum() / 2
            weight = - (returns_ranked - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class ReversalWithoutExtremeValue:

    """price movement coming from market impact should be excluded"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_daily_return_without_extreme_value",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["code", "returns"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="returns")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            returns_mean = returns.mean()
            total_return_avg = returns_mean.mean()
            total_return_sum = returns_mean.apply(lambda x: abs(x)).sum() / 2
            weight = - (returns_mean - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class ReversalWithOnlyExtremeValue:

    """price movement coming from market extreme value is driving return"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_daily_return_without_extreme_value",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["code", "returns"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="returns")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            returns_all = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["open", "close", "code"]) #no cum_adjf for intraday
            returns_all = returns_all.replace(0.,np.nan)
            returns_all["return"] = returns_all["close"] / returns_all["open"] - 1
            returns_all["code"] = returns_all["code"].apply(lambda x: x.decode('utf-8'))
            returns_all = returns_all.pivot_table(index="date", columns="code", values="return")
            returns_all = returns_all.reindex(universe, axis=1).dropna(how="any", axis=1)

            returns = returns_all - returns

            returns_mean = returns.mean()
            total_return_avg = returns_mean.mean()
            total_return_sum = returns_mean.apply(lambda x: abs(x)).sum() / 2
            weight = - (returns_mean - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass

class UpsideDownsideVol:

    """upside downside vol shows momentum / reversal"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_intraday_volatility",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["code", "intraday_vol_up", "intraday_vol_down"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns["intraday_vol_diff"] = returns["intraday_vol_up"] - returns["intraday_vol_down"]
            returns = returns.pivot_table(index="date", columns="code", values="intraday_vol_diff")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            returns_mean = returns.mean()
            total_return_avg = returns_mean.mean()
            total_return_sum = returns_mean.apply(lambda x: abs(x)).sum() / 2
            weight = - (returns_mean - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class WilliamSupport:

    """william support being support"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["code", "close", "low"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns_close = returns.pivot_table(index="date", columns="code", values="close")
            returns_close = returns_close.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns_low = returns.pivot_table(index="date", columns="code", values="low")
            returns_low = returns_low.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns = returns_close - returns_low

            returns_ranked = returns.rank(axis=1).rank(axis=0).tail(1).mean()
            total_return_avg = returns_ranked.mean()
            total_return_sum = returns_ranked.apply(lambda x: abs(x)).sum() / 2
            weight = - (returns_ranked - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class WilliamResistance:

    """william resistance being resistance"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["code", "close", "high"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns_close = returns.pivot_table(index="date", columns="code", values="close")
            returns_close = returns_close.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns_high = returns.pivot_table(index="date", columns="code", values="high")
            returns_high = returns_high.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns = returns_high - returns_close

            returns_ranked = returns.rank(axis=1).rank(axis=0).tail(1).mean()
            total_return_avg = returns_ranked.mean()
            total_return_sum = returns_ranked.apply(lambda x: abs(x)).sum() / 2
            weight = - (returns_ranked - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class WilliamResistanceSupport:

    """william resistance being resistance"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["code", "close", "high", "low"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns_close = returns.pivot_table(index="date", columns="code", values="close")
            returns_close = returns_close.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns_high = returns.pivot_table(index="date", columns="code", values="high")
            returns_high = returns_high.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns_high = returns_high - returns_close
            returns_low = returns.pivot_table(index="date", columns="code", values="low")
            returns_low = returns_low.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns_low = returns_close - returns_low

            returns_ranked = (returns_high / returns_low).rank(axis=1).rank(axis=0).tail(1).mean()
            total_return_avg = returns_ranked.mean()
            total_return_sum = returns_ranked.apply(lambda x: abs(x)).sum() / 2
            weight = - (returns_ranked - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class PositiveVolumeIndex:

    """measuring herd behaviour"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["code", "close", "open", "daily_volume"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns_volume = returns.pivot_table(index="date", columns="code", values="daily_volume")
            returns_volume_diff = returns_volume.diff()
            returns_close = returns.pivot_table(index="date", columns="code", values="close")
            returns_close = returns_close.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns_open = returns.pivot_table(index="date", columns="code", values="open")
            returns_open = returns_open.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns_otc = returns_close / returns_open - 1
            returns_weighted = returns_volume[returns_volume_diff > 0].fillna(0) * returns_otc


            returns_ranked = returns_weighted.tail(1).sum() / returns_volume[returns_volume_diff > 0].mean()
            total_return_avg = returns_ranked.mean()
            total_return_sum = returns_ranked.apply(lambda x: abs(x)).sum() / 2
            weight = - (returns_ranked - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass


class NegativeVolumeIndex:

    """measuring smart money behaviour"""

    def __init__(self, alpha_name, universe, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.data_loader = DataLoader()

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1],
                                                                  ["code", "close", "open", "daily_volume"])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns_volume = returns.pivot_table(index="date", columns="code", values="daily_volume")
            returns_volume_diff = returns_volume.diff()
            returns_close = returns.pivot_table(index="date", columns="code", values="close")
            returns_close = returns_close.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns_open = returns.pivot_table(index="date", columns="code", values="open")
            returns_open = returns_open.reindex(universe, axis=1).dropna(how="any", axis=1)
            returns_otc = returns_close / returns_open - 1
            returns_weighted = returns_volume[returns_volume_diff < 0].fillna(0) * returns_otc

            returns_ranked = returns_weighted.tail(1).sum() / returns_volume[returns_volume_diff < 0].mean()
            total_return_avg = returns_ranked.mean()
            total_return_sum = returns_ranked.apply(lambda x: abs(x)).sum() / 2
            weight = (returns_ranked - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            pass