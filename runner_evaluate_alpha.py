from calcutil.alpha_calc_config import load_config_yaml
from calcutil.alpha_performance_evaluator import PerformanceEvaluator
from data.dataloader import DataLoader
import logging


def merge(dict_list):
    output = []
    for dict_item in dict_list:
        output.extend(list(dict_item.keys()))
    return output

config_file_names = [r"\intraday\momentum_without_intraday_extreme_value.yaml",
                     r"\intraday\intraday_vol_trend.yaml",
                     r"\intraday\volume_consistency.yaml",
                     r"\intraday\momentum_without_intraday_extreme_value.yaml",
                     r"\intraday\momentum_ts_close.yaml",
                     r"\intraday\momentum_max_ratio.yaml",
                     r"\intraday\momentum_change_close.yaml",
                     r"\intraday\momentum_binary_count_close.yaml",
                     ]
alpha_perfmc_cfg_list = merge([load_config_yaml(config) for config in config_file_names])

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    data_loader = DataLoader()
    performance_evaluator = PerformanceEvaluator(data_loader)
    performance_evaluator.evaluate(alpha_perfmc_cfg_list)

