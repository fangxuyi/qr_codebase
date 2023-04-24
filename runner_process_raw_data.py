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
    data_loader = DataLoader()
    dates = data_loader.get_trade_date_between(calc_start, calc_end)

    version = "pv_1min_standard"

    # process raw data
    data_processor = DataProcessor(version, ReferenceDataLoader, RawDataLoader)
    for date in dates:
        logger.info(f"processing {date}...")
        data_processor.process(standard_pv_data_processor, date)

    # load processed
    data_loader = DataLoader()
    data_loader.load_processed("20181210", version, 5)

