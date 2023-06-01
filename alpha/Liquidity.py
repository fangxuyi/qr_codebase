import numpy as np

from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
import pandas as pd
from sklearn.linear_model import LinearRegression


class Liquidity:

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
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="daily_turover")
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


class LiquidityStability:

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
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="daily_turover")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = returns.std()
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


class NormalizedLiquidity:

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
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="daily_turover")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = (returns.tail(1).mean() - returns.mean()) / returns.std()
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


class TurnoverRate:

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
            volume = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            volume["code"] = volume["code"].apply(lambda x: x.decode('utf-8'))
            volume = volume.pivot_table(index="date", columns="code", values="daily_volume")
            volume = volume.reindex(universe, axis=1).dropna(how="any", axis=1)

            neg_shares = self.data_loader.get_market_cap(trade_dates[idx - self.parameter["lookback"]:idx + 1])
            neg_shares["date"] = neg_shares["date"].astype(str)
            neg_shares = neg_shares.pivot_table(index="date", columns="code", values="neg_shares")

            total_return = (volume / neg_shares).mean()
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


class TurnoverRateStability:

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
            volume = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            volume["code"] = volume["code"].apply(lambda x: x.decode('utf-8'))
            volume = volume.pivot_table(index="date", columns="code", values="daily_volume")
            volume = volume.reindex(universe, axis=1).dropna(how="any", axis=1)

            neg_shares = self.data_loader.get_market_cap(trade_dates[idx - self.parameter["lookback"]:idx + 1])
            neg_shares["date"] = neg_shares["date"].astype(str)
            neg_shares = neg_shares.pivot_table(index="date", columns="code", values="neg_shares")

            total_return = (volume / neg_shares).std()
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


class TurnoverRateNormalizedAbs:

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
            turnover_rate = self.data_loader.load_processed_window_list("pv_1min_daily_turnover",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            turnover_rate["code"] = turnover_rate["code"].apply(lambda x: x.decode('utf-8'))
            turnover_rate = turnover_rate.pivot_table(index="date", columns="code", values="abs_return_turnover")
            turnover_rate = turnover_rate.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = (turnover_rate.tail(1).mean() - turnover_rate.mean() )/ turnover_rate.std()
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class TurnoverRateNormalizedUp:

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
            turnover_rate = self.data_loader.load_processed_window_list("pv_1min_daily_turnover",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            turnover_rate["code"] = turnover_rate["code"].apply(lambda x: x.decode('utf-8'))
            turnover_rate = turnover_rate.pivot_table(index="date", columns="code", values="up_return_turnover")
            turnover_rate = turnover_rate.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = (turnover_rate.tail(1).mean() - turnover_rate.mean() )/ turnover_rate.std()
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name)

        except:
            print(f"skipping calc for {self.alpha_name} with lookback {self.parameter['lookback']} on {date}")
            pass


class TurnoverRateNormalizedDown:

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
            turnover_rate = self.data_loader.load_processed_window_list("pv_1min_daily_turnover",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            turnover_rate["code"] = turnover_rate["code"].apply(lambda x: x.decode('utf-8'))
            turnover_rate = turnover_rate.pivot_table(index="date", columns="code", values="down_return_turnover")
            turnover_rate = turnover_rate.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = (turnover_rate.tail(1).mean() - turnover_rate.mean() )/ turnover_rate.std()
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


class TurnoverRateNormalized:

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
            volume = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            volume["code"] = volume["code"].apply(lambda x: x.decode('utf-8'))
            volume = volume.pivot_table(index="date", columns="code", values="daily_volume")
            volume = volume.reindex(universe, axis=1).dropna(how="any", axis=1)

            neg_shares = self.data_loader.get_market_cap(trade_dates[idx - self.parameter["lookback"]:idx + 1])
            neg_shares["date"] = neg_shares["date"].astype(str)
            neg_shares = neg_shares.pivot_table(index="date", columns="code", values="neg_shares")
            turnover_rate = (volume / neg_shares)

            total_return = (turnover_rate.tail(1).mean() - turnover_rate.mean() )/ turnover_rate.std()
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


class TurnoverRateChange:

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
            turnover = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            turnover["code"] = turnover["code"].apply(lambda x: x.decode('utf-8'))
            turnover = turnover.pivot_table(index="date", columns="code", values="daily_turover")
            turnover = turnover.reindex(universe, axis=1).dropna(how="any", axis=1)
            turnover = turnover.applymap(lambda x: np.log(x))

            mkt_val = self.data_loader.get_market_cap(trade_dates[idx - self.parameter["lookback"]:idx + 1])
            mkt_val["date"] = mkt_val["date"].astype(str)
            mkt_val = mkt_val.pivot_table(index="date", columns="code", values="mkt_val")
            mkt_val = mkt_val.applymap(lambda x: np.log(x))

            dataset = pd.concat([turnover.unstack().rename("turnover"),
                                 mkt_val.unstack().rename("market_val")], axis=1)
            dataset = dataset.dropna()
            y = dataset["turnover"].to_numpy()
            x = dataset["market_val"].to_numpy().reshape(-1, 1)
            model = LinearRegression()
            model.fit(x, y)

            dataset = pd.concat([turnover.tail(1).mean().rename("turnover"),
                                 mkt_val.tail(1).mean().rename("market_val")], axis=1)
            dataset = dataset.dropna()
            y_new = dataset["turnover"].to_numpy()
            x_new = dataset["market_val"].to_numpy().reshape(-1, 1)
            y_pred = model.predict(x_new)
            resid = y_new - y_pred
            unexpected_change = pd.Series(resid, index=turnover.tail(1).mean().index)

            total_return = unexpected_change
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


class TurnoverReturns:

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
            pv_1min_return = self.data_loader.load_processed_window_list("pv_1min_standard",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            pv_1min_return["code"] = pv_1min_return["code"].apply(lambda x: x.decode('utf-8'))
            open = pv_1min_return.pivot_table(index="date", columns="code", values="open")
            open = open.reindex(universe, axis=1).dropna(how="any", axis=1)
            close = pv_1min_return.pivot_table(index="date", columns="code", values="close")
            close = close.reindex(universe, axis=1).dropna(how="any", axis=1)

            turnover = pv_1min_return.pivot_table(index="date", columns="code", values="daily_turover")
            turnover = turnover.reindex(universe, axis=1).dropna(how="any", axis=1)

            returns_turnover = (close / open - 1).applymap(abs) * 10 ** (10) / turnover

            total_return = returns_turnover.mean()
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