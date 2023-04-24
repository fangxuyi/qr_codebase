from .utils import *
import logging

logger = logging.getLogger(__name__)


def yyyymmdd_file_to_date(x):
    return int(x.split(r"\\")[-1].replace(".csv", ""))


class ReferenceDataLoader:
    reference_data_path = ReferenceDataPath
    pv_data_path = PVDataPath
    loaded_reference_data = {}

    @classmethod
    def describe_reference_data(cls):
        for ele in cls.loaded_reference_data.keys():
            print(ele)
            print(cls.loaded_reference_data[ele].head())

    @classmethod
    def load_reference_data_by_name(cls, name):
        if name not in cls.loaded_reference_data.keys():
            logger.debug(f"start loading {name}...")
            t = time.perf_counter()
            df = cls.load_reference_data(name)
            cls.loaded_reference_data[name] = df
            logger.debug(f"loaded {name} in {time.perf_counter() - t} seconds")
        return cls.loaded_reference_data[name]

    @classmethod
    def load_all_reference_data(cls):
        logger.debug("start loading reference data...")
        t = time.perf_counter()
        for name in ReferenceData.keys():
            df = cls.load_reference_data(name)
            cls.loaded_reference_data[name] = df
        logger.debug(f"loaded all reference data in {time.perf_counter() - t} seconds")

        return cls.loaded_reference_data

    @classmethod
    def load_reference_data(cls, name, startDate=None, endDate=None):
        directory = ReferenceData[name][0]
        file_pattern = ReferenceData[name][1]

        if r"\yyyy\yyyymmdd.csv" in file_pattern:
            file_pattern = file_pattern.replace(r"\yyyy\yyyymmdd.csv", r"\*\*.csv")
            file = filter_data_loader(yyyymmdd_file_to_date, cls.reference_data_path + directory + file_pattern,
                                      startDate, endDate)
        else:
            file = simple_data_loader(cls.reference_data_path + directory + file_pattern)

        if "code" in file.columns:
            file["code"] = file["code"].astype("int32")
            file["code"] = file["code"].apply(lambda x: '{:06d}'.format(x))

        return file