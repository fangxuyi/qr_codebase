from calcutil.alpha_calc_config import calc_start, calc_end, alpha_calculator_cfg_dict
from calcutil.alpha_calculator import AlphaCalculator
from data.dataloader import DataLoader
import logging


# alpha_list = ["momentum_3_ZZ9999", "momentum_5_ZZ9999", "momentum_10_ZZ9999",
#                          "reversal_10_ZZ9999", "reversal_21_ZZ9999", "reversal_63_ZZ9999",
#                          "open_to_close_reversal_3_ZZ9999","open_to_close_reversal_5_ZZ9999", "open_to_close_reversal_10_ZZ9999", "open_to_close_reversal_21_ZZ9999", "open_to_close_reversal_63_ZZ9999",
#                          "open_to_close_momentum_w_volume_3_ZZ9999", "open_to_close_momentum_w_volume_5_ZZ9999", "open_to_close_momentum_w_volume_10_ZZ9999",
#                          "gapped_reversal_10_ZZ9999", "gapped_reversal_21_ZZ9999", "gapped_reversal_63_ZZ9999",
#                          "ts_momentum_3_ZZ9999", "ts_momentum_5_ZZ9999", "ts_momentum_10_ZZ9999",
#                          "momentum_change_3_ZZ9999", "momentum_change_5_ZZ9999", "momentum_change_10_ZZ9999",
#                          "max_ratio_3_ZZ9999", "max_ratio_5_ZZ9999", "max_ratio_10_ZZ9999",
#                          "binary_count_3_ZZ9999", "binary_count_5_ZZ9999", "binary_count_10_ZZ9999",
#                          "vol_adj_momentum_3_ZZ9999", "vol_adj_momentum_5_ZZ9999", "vol_adj_momentum_10_ZZ9999",
#                          "vol_adj_ts_momentum_3_ZZ9999", "vol_adj_ts_momentum_5_ZZ9999", "vol_adj_ts_momentum_10_ZZ9999",
#                          "ewma_adj_momentum_3_ZZ9999", "ewma_adj_momentum_5_ZZ9999", "ewma_adj_momentum_10_ZZ9999",
#                          "expanded_ts_momentum_3_ZZ9999", "expanded_ts_momentum_5_ZZ9999", "expanded_ts_momentum_10_ZZ9999"]


alpha_list = ["open_to_close_reversal_3_ZZ9999", "open_to_close_reversal_5_ZZ9999", "open_to_close_reversal_10_ZZ9999", "open_to_close_reversal_21_ZZ9999", "open_to_close_reversal_63_ZZ9999"]


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    data_loader = DataLoader()
    dates = data_loader.get_trade_date_between(calc_start, calc_end)

    current_cfg = {alpha: alpha_calculator_cfg_dict[alpha] for alpha in alpha_list}
    AlphaCalculator.alpha_calc(current_cfg, data_loader)

