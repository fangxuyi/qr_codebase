import multiprocessing
from calcutil.alpha_calc_config import pool_size, calc_end
from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
from data.raw_data_loader_settings import *
from data.rawdataloader import RawDataLoader
from data.reference_dataloader import ReferenceDataLoader
import logging


if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    calc_start = "20180101"
    data_loader = DataLoader()
    dates = data_loader.get_trade_date_between(calc_start, calc_end)

    names = ["pv_1min_moneyflow_standard"]
    data_processors = [money_flow_processor]
    data_processor = DataProcessor("multi", ReferenceDataLoader, RawDataLoader)

    args_list = []
    for date in dates:
        args_list.append((names, data_processors, date))

    pool = multiprocessing.Pool(pool_size)
    pool.map(data_processor.process_with_args, args_list)
    pool.close()

# TODO: ADD data validator and error handler

