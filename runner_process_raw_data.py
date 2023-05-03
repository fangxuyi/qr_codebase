from calcutil.alpha_calc_config import calc_start, calc_end
from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
from data.rawdataloader import RawDataLoader
from data.raw_data_loader_settings import *
import logging
from data.reference_dataloader import ReferenceDataLoader

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    calc_start = "20180101"
    data_loader = DataLoader()
    dates = data_loader.get_trade_date_between(calc_start, calc_end)

    version = "pv_1min_high_low_open_close"

    data_processor = DataProcessor(version, ReferenceDataLoader, RawDataLoader)
    for date in dates:
        logger.info(f"processing {date}...")
        data_processor.process(minute_open_high_low_close, date)


    version = "pv_1min_large_small_turnovers"

    data_processor = DataProcessor(version, ReferenceDataLoader, RawDataLoader)
    for date in dates:
        logger.info(f"processing {date}...")
        data_processor.process(big_small_turnover_direction, date)


    version = "pv_1min_daily_return_without_extreme_value"

    data_processor = DataProcessor(version, ReferenceDataLoader, RawDataLoader)
    for date in dates:
        logger.info(f"processing {date}...")
        data_processor.process(momentum_without_extreme_value, date)