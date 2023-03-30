from rawdataloader import RawDataLoader
from dataprocessor import DataProcessor
from settings import *
import logging


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    referenceData = RawDataLoader.load_all_reference_data()
    dataProcessor = DataProcessor(version, referenceData, RawDataLoader)
    dates = referenceData["Calendar"][["date", "is_open"]].astype(int)
    dates = dates[dates["date"] > 20180101]['date'].astype(str).values.tolist()

    for date in dates:
        logger.info(f"processing {date}...")
        dataProcessor.process(standard_pv_data_processor, date)

    # data = dataProcessor.load_processed("20180112", 5)

