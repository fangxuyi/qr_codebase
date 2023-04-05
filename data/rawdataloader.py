from utils import *
import logging

logger = logging.getLogger(__name__)


def yyyymmdd_file_to_date(x):
    return int(x.split(r"\\")[-1].replace(".csv", ""))


def stockid_file_to_date(x):
    return int(x.split("\\")[-2])


class RawDataLoader:
    referenceDataPath = ReferenceDataPath
    pvDataPath = PVDataPath

    @classmethod
    def describe_reference_data(cls, loaded_reference_data):
        for ele in loaded_reference_data.keys():
            print(ele)
            print(loaded_reference_data[ele].head())

    @classmethod
    def load_all_reference_data(cls):
        loaded_reference_data = {}
        logger.debug("start loading reference data...")
        t = time.perf_counter()
        for name in ReferenceData.keys():
            df = cls.load_reference_data(name)
            loaded_reference_data[name] = df
        logger.debug(f"loaded all reference data in {time.perf_counter() - t} seconds")

        return loaded_reference_data

    @classmethod
    def load_pv_data_by_date(cls, startDate=None, endDate=None, pvdatakey="1min_PV"):

        logger.debug("start loading pv data...")
        t = time.perf_counter()
        df = cls.load_pv_data(pvdatakey, startDate, endDate)
        logger.debug(f"loaded pv data between {startDate} and {endDate} in {time.perf_counter() - t} seconds")

        return df

    @classmethod
    def load_reference_data(cls, name, startDate=None, endDate=None):
        directory = ReferenceData[name][0]
        file_pattern = ReferenceData[name][1]

        if r"\yyyy\yyyymmdd.csv" in file_pattern:
            file_pattern = file_pattern.replace(r"\yyyy\yyyymmdd.csv", r"\*\*.csv")
            file = filter_data_loader(yyyymmdd_file_to_date, cls.referenceDataPath + directory + file_pattern,
                                      startDate, endDate)
        else:
            file = simple_data_loader(cls.referenceDataPath + directory + file_pattern)

        if "code" in file.columns:
            file["code"] = file["code"].astype("int32")
            file["code"] = file["code"].apply(lambda x: '{:06d}'.format(x))

        return file

    @classmethod
    def load_pv_data(cls, name, startDate=None, endDate=None):
        directory = PriceData[name][0]
        file_pattern = PriceData[name][1]

        if r"\yyyymmdd\stockid.csv" in file_pattern:
            file_pattern = file_pattern.replace(r"\yyyymmdd\stockid.csv", r"\*\*.csv")
            file = filter_data_loader(stockid_file_to_date, cls.pvDataPath + directory + file_pattern, startDate,
                                      endDate)
        else:
            file = simple_data_loader(cls.pvDataPath + directory + file_pattern)

        if "code" in file.columns:
            file["code"] = file["code"].astype("int32")
            file["code"] = file["code"].apply(lambda x: '{:06d}'.format(x))

        return file