import itertools

from calcutil.alpha_calc_config import calc_start, calc_end, universe_options, pool_size
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
    def calc_alpha_for_date(cls, args):
        t = time.perf_counter()
        instance = args[0]
        date = args[1]
        result = instance.calculate(date)
        return result

    @classmethod
    def alpha_calc(cls, cfg_dict, data_loader):

        cls.validate_config(cfg_dict)
        trade_dates = data_loader.get_trade_date_between(calc_start, calc_end)

        instances = []
        for key, value in cfg_dict.items():
            alpha_name = key
            class_name = value[cls.class_name_string]
            universe = value[cls.universe_string]
            parameters = value[cls.parameters_string]

            cls_names = class_name.split(".")
            class_ = getattr(__import__("alpha." + cls_names[0]), cls_names[0])
            for ele in cls_names[1:]:
                class_ = getattr(class_, ele)
            instance = class_(alpha_name, universe, parameters)
            instances.append(instance)

        args = list(itertools.product(instances, trade_dates))

        pool = multiprocessing.Pool(pool_size)
        pool.map(cls.calc_alpha_for_date, args)
        pool.close()

        logger.info("done calculating all alpha.")
