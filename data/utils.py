from data.raw_data_loader_settings import *
import dask.dataframe as dd
import glob
import logging
import pandas as pd
import re
import time

logger = logging.getLogger(__name__)


def read_csv(filenames, **kwargs):
    return read_csv_pandas(filenames, **kwargs)


def read_csv_pandas(filenames, **kwargs):
    if isinstance(filenames, str):
        filenames = [filenames]
    output = []
    t = time.perf_counter()
    for filename in filenames:
        df = pd.read_csv(filename, **kwargs)
        date_matched = re.search(r"\d{4}(0[1-9]|1[012])(0[1-9]|[12][0-9]|3[01])", filename)
        date_matched = "None" if date_matched is None else date_matched[0]
        df["date_int"] = int(date_matched)
        df["path"] = filename
        output.append(df)
    if len(output) > 0:
        df = pd.concat(output)
    else:
        df = pd.DataFrame(columns=PriceDataColumns)
    logger.debug(f"load {len(filenames)} files in {time.perf_counter() - t}")
    return df


def read_csv_dask(filenames, **kwargs):
    t = time.perf_counter()
    df = dd.read_csv(filenames, assume_missing=True, **kwargs)
    logger.debug(f"load {len(filenames)} files in {time.perf_counter() - t}")
    return df


def simple_data_loader(directory, **kwargs):
    logger.debug(f"loading from {directory}")

    return read_csv(directory, **kwargs)


def filter_data_loader(func, directory, startDate=None, endDate=None, **kwargs):
    """Dates are inclusive"""
    logger.debug(f"loading from {directory}")
    allfiles = glob.glob(directory, recursive=True)
    logger.debug(f"all files {allfiles}")

    if startDate is not None:
        allfiles = [ele for ele in allfiles if func(ele) >= int(startDate)]

    if endDate is not None:
        allfiles = [ele for ele in allfiles if func(ele) <= int(startDate)]

    return read_csv(allfiles, **kwargs)

