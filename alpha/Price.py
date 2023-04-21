import numpy as np

from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
import pandas as pd


class Momentum:

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass


class Reversal:

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass


class GappedReversal:

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass


class TimeSeriesMomentum:

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass


class MomentumChange:

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass


class MaxRatio:

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass


class BinaryCount:

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass


class VolAdjMomentum:

    """large return should be more significant for low vol period: continuously moving up is more valuable"""

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass


class VolAdjTSMomentum:

    """time series variation adjusted by volatility: change in low vol period is more valuable"""

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass


class EWMAAdjMomentum:

    """recent price action is more valuable"""

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass


class ExpandedTimeSeriesMomentum:

    """smooth out recent price movement noise"""

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

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
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass