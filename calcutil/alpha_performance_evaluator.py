from calcutil.alpha_calc_config import calc_start, calc_end, pool_size
from data.dataloader import DataLoader
import logging
import multiprocessing
import pandas as pd
import time

from data.dataprocessor import DataProcessor

logger = logging.getLogger(__name__)


class PerformanceEvaluator:

    def __init__(self, reference_data):
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

    def evaluate(self, alpha_list):
        pool = multiprocessing.Pool(pool_size)
        pool.map(self.evaluate_single_alpha, alpha_list)
        pool.close()

    def evaluate_single_alpha(self, alpha_name):
        t = time.perf_counter()
        trade_dates = self.data_loader.get_trade_date_between(calc_start,calc_end)
        alpha = self.data_loader.load_processed_alpha(alpha_name)
        returns = self.dataloader.load_processed("1min_PV_return", trade_dates)
        merged_return = pd.merge(alpha, returns, left_on=["code", "date"], right_on=["code", "date"], how="left")
        merged_return["contributed_return"] = merged_return["return"] * merged_return["weight"]
        DataProcessor.write_performance_data(alpha_name, merged_return)
        logger.info(f"calculated performance for {alpha_name} in {time.perf_counter() - t} seconds")

