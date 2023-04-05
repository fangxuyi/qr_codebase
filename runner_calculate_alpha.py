from alphautil.alpha_calc_config import calc_start, calc_end, alpha_calculator_cfg_dict
from alphautil.alpha_calculator import AlphaCalculator
from data.dataloader import DataLoader
from data.rawdataloader import RawDataLoader
import logging


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    dates = DataLoader.get_trade_date_between(calc_start, calc_end)

    reference_data = RawDataLoader.load_all_reference_data()

    AlphaCalculator.alpha_calc(alpha_calculator_cfg_dict, reference_data)

