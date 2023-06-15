from calcutil.alpha_calc_config import load_config_yaml, ConfigPath
from calcutil.alpha_performance_evaluating_util import PerformanceEvaluatingUtils
from calcutil.alpha_performance_evaluator import PerformanceEvaluator
from data.dataloader import DataLoader
import logging


def merge(dict_list):
    output = []
    for dict_item in dict_list:
        output.extend(list(dict_item.keys()))
    return output

config_file_names = [
                       r"\intraday\large_money_flow.yaml",
                       # r"\intraday\large_money_flow_percent.yaml",
                       # r"\intraday\large_money_flow_ratio.yaml",
                       # r"\intraday\medium_money_flow.yaml",
                       # r"\intraday\medium_money_flow_percent.yaml",
                       # r"\intraday\medium_money_flow_ratio.yaml",
                       # r"\intraday\mega_money_flow.yaml",
                       # r"\intraday\mega_money_flow_percent.yaml",
                       # r"\intraday\mega_money_flow_ratio.yaml",
                       # r"\intraday\small_money_flow.yaml",
                       # r"\intraday\small_money_flow_percent.yaml",
                       # r"\intraday\small_money_flow_ratio.yaml",
                     ]

# import glob
# config_file_names = [ele.replace(ConfigPath, "") for ele in glob.glob(ConfigPath+r"\*\*.yaml")]

alpha_perfmc_cfg_list = merge([load_config_yaml(config) for config in config_file_names])

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    data_loader = DataLoader()
    alpha_performance_evaluating_utils = PerformanceEvaluatingUtils(data_loader)
    performance_evaluator = PerformanceEvaluator(alpha_performance_evaluating_utils)
    performance_evaluator.evaluate(alpha_perfmc_cfg_list)

