from calcutil.alpha_calc_config import alpha_perfmc_cfg_list
from calcutil.alpha_performance_evaluator import PerformanceEvaluator
from data.rawdataloader import RawDataLoader
import logging


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    reference_data = RawDataLoader.load_all_reference_data()
    performance_evaluator = PerformanceEvaluator(reference_data)
    performance_evaluator.evaluate(alpha_perfmc_cfg_list)

