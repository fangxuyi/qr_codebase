from dataloader import DataLoader
import alpha
import logging
import multiprocessing
import time

logger = logging.getLogger(__name__)


class AlphaCalculator:
    calc_start = "20180101"
    calc_end = "20201231"
    class_name_string = "classname"
    universe_string = "universe"
    parameters_string = "parameters"

    @classmethod
    def alpha_calc(cls, cfg_dict, reference_data):

        trade_dates = DataLoader.get_trade_date_between(reference_data, int(cls.calc_start), int(cls.calc_end))

        for key, value in cfg_dict.items():
            t = time.perf_counter()
            alpha_name = key
            class_name = value[cls.class_name_string]
            universe = value[cls.universe_string]
            parameters = value[cls.parameters_string]

            module = __import__(alpha)
            class_ = getattr(module, class_name)
            instance = class_(alpha_name, universe, reference_data, **parameters)

            pool = multiprocessing.Pool(16)
            pool.map(instance.calculate, trade_dates)
            pool.close()
            logger.info(f"calculated alpha in {time.perf_counter() - t} seconds")

        logger.info("done calculating all alpha.")
