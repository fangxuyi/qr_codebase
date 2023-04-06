from calcutil.alpha_calc_config import calc_start, calc_end, pool_size
from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
import logging
import multiprocessing
import numpy as np
import pandas as pd
import quantstats as qs
import time

from data.raw_data_loader_settings import TearSheetOutputPath

logger = logging.getLogger(__name__)
qs.extend_pandas()


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
        merged_alpha.loc[merged_alpha["is_halt"], "return"] = np.nan
        merged_alpha = merged_alpha.pivot_table(index="date", columns="code", values="return").ffill()
        return merged_alpha.stack()

    def evaluate_single_alpha(self, alpha_name):
        t = time.perf_counter()
        trade_dates = self.data_loader.get_trade_date_between(calc_start, calc_end)
        alpha = self.data_loader.load_processed_alpha(alpha_name)
        halt_adj_alpha = self.adjust_halt(alpha)
        returns = self.dataloader.load_processed_window_list("pv_1min_return", trade_dates)
        merged_return = pd.merge(halt_adj_alpha, returns, left_on=["code", "date"], right_on=["code", "date"],
                                 how="left")
        merged_return["contributed_return"] = merged_return["return"] * merged_return["weight"]
        DataProcessor.write_performance_data(alpha_name, merged_return)
        return_series = merged_return[["date", "contributed_return"]].groupby("date").sum()
        return_series.index = pd.to_datetime(return_series.index)
        qs.reports.html(return_series, output=True, download_filename=TearSheetOutputPath + f"\\{alpha_name}.html")
        logger.info(f"calculated performance for {alpha_name} in {time.perf_counter() - t} seconds")
