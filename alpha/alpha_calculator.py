from alpha.alpha_calc_config import calc_start, calc_end, universe_options
from data.dataloader import DataLoader
import alpha
import logging
import multiprocessing
import time

logger = logging.getLogger(__name__)


class AlphaCalculator:
    class_name_string = "classname"
    universe_string = "universe"
    parameters_string = "parameters"

    @classmethod
    def validate_config(cls, cfg_dict):
        for key, value in cfg_dict.items():
            assert cls.class_name_string in value.keys(), f"[classname] is a required config parameter for alpha {key}"
            assert cls.universe_string in value.keys(), f"[universe] is a required config parameter for alpha {key}"
            assert cls.parameters_string in value.keys(), f"[parameters] is a required config parameter for alpha {key}"
            assert value[cls.universe_string] in universe_options, f"[universe] is required to be one of {universe_options} while input is {value[cls.universe_string]}"

    @classmethod
    def alpha_calc(cls, cfg_dict, reference_data):

        cls.validate_config(cfg_dict)
        trade_dates = DataLoader.get_trade_date_between(reference_data, int(calc_start), int(calc_end))

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
