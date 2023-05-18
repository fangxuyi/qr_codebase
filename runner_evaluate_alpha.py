from calcutil.alpha_calc_config import load_config_yaml
from calcutil.alpha_performance_evaluator import PerformanceEvaluator
from data.dataloader import DataLoader
import logging


def merge(dict_list):
    output = []
    for dict_item in dict_list:
        output.extend(list(dict_item.keys()))
    return output

config_file_names = [
                     r"\intraday\intraday_negative_volume.yaml",
                     r"\daily\reversal_william_resistance_support.yaml",
                     r"\intraday\intraday_strength.yaml",
                     r"\intraday\reversal_vwap.yaml",
                     ]
alpha_perfmc_cfg_list = merge([load_config_yaml(config) for config in config_file_names])

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    data_loader = DataLoader()
    performance_evaluator = PerformanceEvaluator(data_loader)
    performance_evaluator.evaluate(alpha_perfmc_cfg_list)

