import numpy as np
import pandas as pd


def turnover(returns):
    turnover = returns.pivot_table(index="date", columns="code", values="weight")
    return turnover.diff().apply(abs).sum(axis=1)


def longside_return(returns):
    returns = returns[returns["weight"] > 0]
    return returns[["date", "contributed_return"]].groupby("date").sum()["contributed_return"]


def shortside_return(returns):
    returns = returns[returns["weight"] < 0]
    return returns[["date", "contributed_return"]].groupby("date").sum()["contributed_return"]


class PerformanceEvaluatingUtils:

    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.delayed_return_config = [0, 3, 5, 10, 21]

    def adjust_halt(self, alpha):

        halt_dt = self.data_loader.get_halt_date()
        merged_alpha = pd.merge(alpha, halt_dt, left_on=["code", "date"], right_on=["code", "date"], how="left")
        merged_alpha = merged_alpha.fillna(0)
        merged_alpha.loc[merged_alpha["is_halt"] == 1, "weight"] = np.nan
        merged_alpha = merged_alpha.pivot_table(index="date", columns="code", values="weight").ffill()
        return merged_alpha.stack()

    def get_delay_n_alpha(self, alpha, n):

        alpha = alpha.pivot_table(index="date", columns="code", values="weight").shift(n).stack().rename("weight").reset_index()
        halt_adj_alpha = self.adjust_halt(alpha).rename("weight").reset_index()
        delay_n_alpha = halt_adj_alpha.pivot_table(index="date", columns="code", values="weight").shift(1)
        delay_n_alpha = delay_n_alpha.stack().rename("weight").reset_index()
        return delay_n_alpha

    def calculate_delay_n_alpha_returns(self, alpha, returns, n):

        delayed_alpha = self.get_delay_n_alpha(alpha, n)
        merged_return = pd.merge(delayed_alpha, returns, left_on=["code", "date"], right_on=["code", "date"],
                                 how="left")
        merged_return["contributed_return"] = merged_return["return"] * merged_return["weight"]
        return merged_return

    def calculate_all_delayed_returns(self, alpha, returns):

        delayed_alpha = self.get_delay_n_alpha(alpha, 1)
        delay_1_returns = pd.merge(delayed_alpha, returns, left_on=["code", "date"], right_on=["code", "date"],
                                 how="left")
        delay_1_returns["contributed_return"] = delay_1_returns["return"] * delay_1_returns["weight"]
        delay_1_returns = delay_1_returns[["date", "contributed_return"]].groupby("date").sum()
        delay_1_returns.index = pd.to_datetime(delay_1_returns.index.astype(str))

        output = []
        for ele in self.delayed_return_config:
            delayed_alpha = self.get_delay_n_alpha(alpha, ele)
            merged_return = pd.merge(delayed_alpha, returns, left_on=["code", "date"], right_on=["code", "date"],
                                     how="left")
            merged_return["contributed_return"] = merged_return["return"] * merged_return["weight"]
            merged_return = merged_return[["date", "contributed_return"]].groupby("date").sum()
            merged_return.index = pd.to_datetime(merged_return.index.astype(str))
            output.append(merged_return["contributed_return"].rename("delay " + str(ele)))
        output = pd.concat(output, axis=1)
        return delay_1_returns, output


