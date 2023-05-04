from calcutil.alpha_performance_evaluator import PerformanceEvaluator
from data.dataloader import DataLoader
import logging

alpha_perfmc_cfg_list = [
                         "open_to_close_reversal_3_ZZ9999", "open_to_close_reversal_63_ZZ9999", "open_to_close_momentum_w_volume_corr_21_ZZ9999",
                         "top_bottom_return_reversal_1_ZZ9999", "top_bottom_return_reversal_2_ZZ9999",
                         "top_bottom_return_reversal_3_ZZ9999",
                         "top_bottom_return_reversal_5_ZZ9999", "top_bottom_return_reversal_10_ZZ9999",
                         "top_bottom_return_reversal_21_ZZ9999",
                         "top_bottom_return_reversal_63_ZZ9999",
                         "ranked_short_term_low_reserval_3_ZZ9999", "ranked_short_term_low_reserval_5_ZZ9999", "ranked_short_term_low_reserval_10_ZZ9999",
                         "ranked_short_term_low_reserval_21_ZZ9999", "ranked_short_term_low_reserval_63_ZZ9999"
]

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    data_loader = DataLoader()
    performance_evaluator = PerformanceEvaluator(data_loader)
    performance_evaluator.evaluate(alpha_perfmc_cfg_list)

