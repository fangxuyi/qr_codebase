import numpy as np
import pandas as pd


class PerformanceEvaluatingUtils:

    def __init__(self, data_loader):
        self.data_loader = data_loader
        self.delayed_return_config = [0, 3, 5, 10, 21]

    def adjust_halt(self, alpha):

        halt_dt = self.data_loader.get_halt_date()
        merged_alpha = pd.merge(alpha, halt_dt, left_on=["code", "date"], right_on=["code", "date"], how="left")
        merged_alpha_is_halt = merged_alpha.pivot_table(index="date", columns="code", values="is_halt").fillna(0)
        merged_alpha_weight = merged_alpha.pivot_table(index="date", columns="code", values="weight").fillna(0)
        merged_alpha_weight[merged_alpha_is_halt == 1] = np.nan
        merged_alpha = merged_alpha_weight.ffill()
        return merged_alpha.stack()

    def adjust_limit(self, alpha, limit):

        limit_stack = limit.stack().rename("limit").reset_index()
        merged_alpha = pd.merge(alpha, limit_stack, left_on=["code", "date"], right_on=["code", "date"], how="left")
        merged_alpha_is_limit = merged_alpha.pivot_table(index="date", columns="code", values="limit").fillna(0)
        merged_alpha_weight = merged_alpha.pivot_table(index="date", columns="code", values="weight").fillna(0)
        merged_alpha_weight[merged_alpha_is_limit == 1] = np.nan
        merged_alpha = merged_alpha_weight.ffill()
        return merged_alpha.stack()

    def get_delay_n_alpha(self, alpha, n, limit):

        alpha = alpha.pivot_table(index="date", columns="code", values="weight").shift(n).stack().rename("weight").reset_index()
        halt_adj_alpha = self.adjust_halt(alpha).rename("weight").reset_index()
        limit_adj_alpha = self.adjust_limit(halt_adj_alpha, limit).rename("weight").reset_index()
        delay_n_alpha = limit_adj_alpha.pivot_table(index="date", columns="code", values="weight").shift(1)
        delay_n_alpha = delay_n_alpha.stack().rename("weight").reset_index()
        return delay_n_alpha

    def calculate_delay_n_alpha_returns(self, alpha, returns, n, limit):

        delayed_alpha = self.get_delay_n_alpha(alpha, n, limit)
        merged_return = pd.merge(delayed_alpha, returns, left_on=["code", "date"], right_on=["code", "date"],
                                 how="left")
        merged_return["contributed_return"] = merged_return["return"] * merged_return["weight"]
        return merged_return

    def calculate_all_delayed_returns(self, alpha, returns, limit):

        delayed_alpha = self.get_delay_n_alpha(alpha, 1, limit)
        delay_1_returns = pd.merge(delayed_alpha, returns, left_on=["code", "date"], right_on=["code", "date"],
                                 how="left")
        delay_1_returns["contributed_return"] = delay_1_returns["return"] * delay_1_returns["weight"]

        output = []
        for ele in self.delayed_return_config:
            delayed_alpha = self.get_delay_n_alpha(alpha, ele, limit)
            merged_return = pd.merge(delayed_alpha, returns, left_on=["code", "date"], right_on=["code", "date"],
                                     how="left")
            merged_return["contributed_return"] = merged_return["return"] * merged_return["weight"]
            merged_return = merged_return[["date", "contributed_return"]].groupby("date").sum()
            merged_return.index = pd.to_datetime(merged_return.index.astype(str))
            output.append(merged_return["contributed_return"].rename("delay " + str(ele)))
        output = pd.concat(output, axis=1)
        return delay_1_returns, output


