from calcutil import reports
from calcutil.alpha_calc_config import calc_start, calc_end, pool_size
from data.dataprocessor import DataProcessor
import logging
import multiprocessing
import pandas as pd
import quantstats as qs
import time

from data.raw_data_loader_settings import TearSheetOutputPath, DataPath

logger = logging.getLogger(__name__)
qs.extend_pandas()


class PerformanceEvaluator:

    def __init__(self, alpha_performance_evaluating_utils):
        self.alpha_performance_evaluating_utils = alpha_performance_evaluating_utils

    def evaluate(self, alpha_list):
        pool = multiprocessing.Pool(pool_size)
        all_returns = pool.map(self.evaluate_single_alpha, alpha_list)
        print("***** correlation matrix *****")
        pd.concat(all_returns, axis=1).corr().to_csv(DataPath + "\\" + "correlation.csv")
        pool.close()

        # all_returns = [self.evaluate_single_alpha(alpha) for alpha in alpha_list]
        # pd.concat(all_returns, axis=1).corr().to_csv(DataPath + "\\" + "correlation.csv")

    def evaluate_single_alpha(self, alpha_name):
        t = time.perf_counter()
        trade_dates = self.alpha_performance_evaluating_utils.data_loader.get_trade_date_between(calc_start, calc_end)
        alpha = self.alpha_performance_evaluating_utils.data_loader.load_processed_alpha_window_list(alpha_name, trade_dates)
        alpha["code"] = alpha["code"].apply(lambda x: x.decode('utf-8'))

        returns = self.alpha_performance_evaluating_utils.data_loader.load_processed_window_list("pv_1min_return", trade_dates)
        returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
        returns["date"] = returns["date"].astype(int)

        delay_1, all_returns = self.alpha_performance_evaluating_utils.calculate_all_delayed_returns(alpha, returns)
        delay_1_returns = delay_1[["date", "contributed_return"]].groupby("date").sum()
        delay_1_returns.index = pd.to_datetime(delay_1_returns.index.astype(str))

        delay_1_returns_details = delay_1.pivot_table(index="date", columns="code", values="return")
        delay_1_returns_details.index = pd.to_datetime(delay_1_returns_details.index.astype(str))
        delay_1_weights = delay_1.pivot_table(index="date", columns="code", values="weight")
        delay_1_weights.index = pd.to_datetime(delay_1_weights.index.astype(str))
        DataProcessor.write_performance_data(alpha_name, delay_1)

        reports.html(delay_1_returns["contributed_return"], all_returns, delay_1_weights, delay_1_returns_details, output=True,
                                 download_filename=TearSheetOutputPath + f"\\{alpha_name}.html")
        logger.info(f"calculated performance for {alpha_name} in {time.perf_counter() - t} seconds")

        return delay_1_returns["contributed_return"].rename(alpha_name)
