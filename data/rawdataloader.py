from .utils import *
import logging

logger = logging.getLogger(__name__)



def stockid_file_to_date(x):
    return int(x.split("\\")[-2])


class RawDataLoader:
    referenceDataPath = ReferenceDataPath
    pvDataPath = PVDataPath

    @classmethod
    def load_pv_data_by_date(cls, startDate=None, endDate=None, pvdatakey="1min_PV"):

        logger.debug("start loading pv data...")
        t = time.perf_counter()
        df = cls.load_pv_data(pvdatakey, startDate, endDate)
        logger.debug(f"loaded pv data between {startDate} and {endDate} in {time.perf_counter() - t} seconds")

        return df

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