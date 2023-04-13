from calcutil.alpha_calc_config import calc_start, calc_end, pool_size
from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
import logging
import multiprocessing
import numpy as np
import pandas as pd
import quantstats as qs
import time

from data.raw_data_loader_settings import TearSheetOutputPath, OtherPerfOutputPath

logger = logging.getLogger(__name__)
qs.extend_pandas()


def turnover(returns):
    turnover = returns.pivot_table(index="date", columns="code", values="weight")
    return turnover.diff().apply(abs).sum(axis=1)


def longside_return(returns):
    returns = returns[returns["weight"] > 0]
    return returns[["date", "contributed_return"]].groupby("date").sum()["contributed_return"]


def shortside_return(returns):
    returns = returns[returns["weight"] < 0]
    return returns[["date", "contributed_return"]].groupby("date").sum()["contributed_return"]


class PerformanceEvaluator:

    def __init__(self, reference_data):
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

    def evaluate(self, alpha_list):
        pool = multiprocessing.Pool(pool_size)
        pool.map(self.evaluate_single_alpha, alpha_list)
        pool.close()

    def adjust_halt(self, alpha):
        halt_dt = self.data_loader.get_halt_date()
        merged_alpha = pd.merge(alpha, halt_dt, left_on=["code", "date"], right_on=["code", "date"], how="left")
        merged_alpha = merged_alpha.fillna(0)
        merged_alpha.loc[merged_alpha["is_halt"] == 1, "weight"] = np.nan
        merged_alpha = merged_alpha.pivot_table(index="date", columns="code", values="weight").ffill()
        return merged_alpha.stack()

    def evaluate_single_alpha(self, alpha_name):
        t = time.perf_counter()
        trade_dates = self.data_loader.get_trade_date_between(calc_start, calc_end)
        alpha = self.data_loader.load_processed_alpha(alpha_name)
        alpha["code"] = alpha["code"].apply(lambda x: x.decode('utf-8'))
        halt_adj_alpha = self.adjust_halt(alpha).rename("weight").reset_index()

        # delay 1: getting weight eod day T, trade in T+1, get return T+2
        delay_1_alpha = halt_adj_alpha.pivot_table(index="date", columns="code", values="weight").shift(2)
        delay_1_alpha = delay_1_alpha.stack().rename("weight").reset_index()

        returns = self.data_loader.load_processed_window_list("pv_1min_return", trade_dates)
        returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
        returns["date"] = returns["date"].astype(int)
        merged_return = pd.merge(delay_1_alpha, returns, left_on=["code", "date"], right_on=["code", "date"],
                                 how="left")
        merged_return["contributed_return"] = merged_return["return"] * merged_return["weight"]

        DataProcessor.write_performance_data(alpha_name, merged_return)
        return_series = merged_return[["date", "contributed_return"]].groupby("date").sum()
        return_series.index = pd.to_datetime(return_series.index.astype(str))

        qs.reports.html(return_series["contributed_return"], output=True,
                        download_filename=TearSheetOutputPath + f"\\{alpha_name}.html")
        other_metrics = pd.concat([turnover(merged_return).rename("turnover"),
                                   longside_return(merged_return).rename("longside_return"),
                                   shortside_return(merged_return).rename("shortside_return")], axis=1)
        other_metrics.to_csv(OtherPerfOutputPath + f"\\{alpha_name}.csv")
        logger.info(f"calculated performance for {alpha_name} in {time.perf_counter() - t} seconds")
