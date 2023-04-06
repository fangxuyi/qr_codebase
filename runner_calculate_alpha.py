from calcutil.alpha_calc_config import calc_start, calc_end, alpha_calculator_cfg_dict
from calcutil.alpha_calculator import AlphaCalculator
from data.dataloader import DataLoader
from data.rawdataloader import RawDataLoader
import logging


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    reference_data = RawDataLoader.load_all_reference_data()
    data_loader = DataLoader(reference_data)
    dates = data_loader.get_trade_date_between(calc_start, calc_end)

    AlphaCalculator.alpha_calc(alpha_calculator_cfg_dict, reference_data, data_loader)

