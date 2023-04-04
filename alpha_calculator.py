import logging
import alpha
from dataprocessor import DataProcessor
from dataloader import DataLoader
from settings import FileOrgStructure, AlphaOutputPath

logger = logging.getLogger(__name__)


class AlphaCalculator:
    calc_start = "20180101"
    calc_end = "20201231"
    output_path = AlphaOutputPath
    class_name_string = "classname"
    universe_string = "universe"
    parameters_string = "parameters"

    @classmethod
    def alpha_calc(cls, cfg_dict, reference_data):

        logger.info("start calculating alpha...")

        trade_dates = DataLoader.get_trade_date_between(reference_data, int(cls.calc_start), int(cls.calc_end))

        for key, value in cfg_dict.items():

            alpha_name = key
            class_name = value[cls.class_name_string]
            universe = value[cls.universe_string]
            parameters = value[cls.parameters_string]

            module = __import__(alpha)
            class_ = getattr(module, class_name)
            instance = class_(alpha_name, universe, reference_data, **parameters)
            for i in range(0, len(trade_dates)):
                date = trade_dates[i]
                result = instance.calculate(date)
                DataProcessor.write_data(date, result, FileOrgStructure.DATECOLUMN, cls.output_path, instance.name)

        logger.info("done calculating alpha.")
