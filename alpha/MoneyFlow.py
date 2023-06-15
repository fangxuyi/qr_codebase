import numpy as np

from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
import pandas as pd


class MegaOrderFlowRatio:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            inflow = returns.pivot_table(index="date", columns="code", values="ultra_large_in")
            outflow = returns.pivot_table(index="date", columns="code", values="ultra_large_out")
            returns = (inflow - outflow) / (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class LargeOrderFlowRatio:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            inflow = returns.pivot_table(index="date", columns="code", values="large_in")
            outflow = returns.pivot_table(index="date", columns="code", values="large_out")
            returns = (inflow - outflow) / (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class MediumOrderFlowRatio:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            inflow = returns.pivot_table(index="date", columns="code", values="medium_in")
            outflow = returns.pivot_table(index="date", columns="code", values="medium_out")
            returns = (inflow - outflow) / (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class SmallOrderFlowRatio:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            inflow = returns.pivot_table(index="date", columns="code", values="small_in")
            outflow = returns.pivot_table(index="date", columns="code", values="small_out")
            returns = (inflow - outflow) / (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class MegaOrderFlow:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            inflow = returns.pivot_table(index="date", columns="code", values="ultra_large_in")
            outflow = returns.pivot_table(index="date", columns="code", values="ultra_large_out")
            returns = (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class LargeOrderFlow:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            inflow = returns.pivot_table(index="date", columns="code", values="large_in")
            outflow = returns.pivot_table(index="date", columns="code", values="large_out")
            returns = (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class MediumOrderFlow:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            inflow = returns.pivot_table(index="date", columns="code", values="medium_in")
            outflow = returns.pivot_table(index="date", columns="code", values="medium_out")
            returns = (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class SmallOrderFlow:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            inflow = returns.pivot_table(index="date", columns="code", values="small_in")
            outflow = returns.pivot_table(index="date", columns="code", values="small_out")
            returns = (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class SmallOrderFlowPercent:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))

            returns["total_in"] = returns["small_in"] + returns["medium_in"] + returns["large_in"] + returns["ultra_large_in"]
            returns["total_out"] = returns["small_out"] + returns["medium_out"] + returns["large_out"] + returns["ultra_large_out"]
            returns["small"] = returns["small_out"] + returns["small_in"]

            inflow = returns.pivot_table(index="date", columns="code", values="total_in")
            outflow = returns.pivot_table(index="date", columns="code", values="total_out")
            binflow = returns.pivot_table(index="date", columns="code", values="small")
            returns = binflow / (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class MediumOrderFlowPercent:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))

            returns["total_in"] = returns["small_in"] + returns["medium_in"] + returns["large_in"] + returns["ultra_large_in"]
            returns["total_out"] = returns["small_out"] + returns["medium_out"] + returns["large_out"] + returns["ultra_large_out"]
            returns["medium"] = returns["medium_out"] + returns["medium_in"]

            inflow = returns.pivot_table(index="date", columns="code", values="total_in")
            outflow = returns.pivot_table(index="date", columns="code", values="total_out")
            binflow = returns.pivot_table(index="date", columns="code", values="medium")
            returns = binflow / (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass



class LargeOrderFlowPercent:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))

            returns["total_in"] = returns["small_in"] + returns["medium_in"] + returns["large_in"] + returns["ultra_large_in"]
            returns["total_out"] = returns["small_out"] + returns["medium_out"] + returns["large_out"] + returns["ultra_large_out"]
            returns["large"] = returns["large_out"] + returns["large_in"]

            inflow = returns.pivot_table(index="date", columns="code", values="total_in")
            outflow = returns.pivot_table(index="date", columns="code", values="total_out")
            binflow = returns.pivot_table(index="date", columns="code", values="large")
            returns = binflow / (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class MegaOrderFlowPercent:

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
            returns = self.data_loader.load_processed_window_list("pv_1min_moneyflow_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))

            returns["total_in"] = returns["small_in"] + returns["medium_in"] + returns["large_in"] + returns["ultra_large_in"]
            returns["total_out"] = returns["small_out"] + returns["medium_out"] + returns["large_out"] + returns["ultra_large_out"]
            returns["ultra_large"] = returns["ultra_large_out"] + returns["ultra_large_in"]

            inflow = returns.pivot_table(index="date", columns="code", values="total_in")
            outflow = returns.pivot_table(index="date", columns="code", values="total_out")
            binflow = returns.pivot_table(index="date", columns="code", values="ultra_large")
            returns = binflow / (inflow + outflow)
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
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass