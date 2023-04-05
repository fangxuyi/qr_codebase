from alphautil.alpha_calc_config import calc_start, calc_end
from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
from data.rawdataloader import RawDataLoader
from data.raw_data_loader_settings import *
import logging


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)
    dates = DataLoader.get_trade_date_between(calc_start, calc_end)

    referenceData = RawDataLoader.load_all_reference_data()

    # process raw data
    dataProcessor = DataProcessor(version, referenceData, RawDataLoader)
    for date in dates:
        logger.info(f"processing {date}...")
        dataProcessor.process(standard_pv_data_processor, date)

    # load processed
    dataLoader = DataLoader(referenceData)
    dataLoader.load_processed("20181210", version, 5)

