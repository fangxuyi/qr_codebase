from calcutil.alpha_calc_config import calc_start, calc_end, load_config_yaml
from calcutil.alpha_calculator import AlphaCalculator
from data.dataloader import DataLoader
import logging


def merge(dict_list):
    merged_dict = {}
    for dict_item in dict_list:
        merged_dict.update(dict_item)
    return merged_dict


config_file_names = [
                       r"\intraday\large_money_flow.yaml",
                       r"\intraday\large_money_flow_percent.yaml",
                       r"\intraday\large_money_flow_ratio.yaml",
                       r"\intraday\medium_money_flow.yaml",
                       r"\intraday\medium_money_flow_percent.yaml",
                       r"\intraday\medium_money_flow_ratio.yaml",
                       r"\intraday\mega_money_flow.yaml",
                       r"\intraday\mega_money_flow_percent.yaml",
                       r"\intraday\mega_money_flow_ratio.yaml",
                       r"\intraday\small_money_flow.yaml",
                       r"\intraday\small_money_flow_percent.yaml",
                       r"\intraday\small_money_flow_ratio.yaml",
                     ]

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    data_loader = DataLoader()
    dates = data_loader.get_trade_date_between(calc_start, calc_end)
    config_file_dict = [load_config_yaml(config) for config in config_file_names]
    current_cfg = merge(config_file_dict)
    AlphaCalculator.alpha_calc(current_cfg, data_loader)

