from logging import handlers
from settings import *
import h5py
import logging
import numpy as np
import pandas as pd
import time

fh = handlers.RotatingFileHandler(WARNING_LOGFILE.format(version), maxBytes=(1048576 * 5), backupCount=7)
logger = logging.getLogger(__name__)
logger.addHandler(fh)


class DataProcessor:

    def __init__(self, name, referenceData, RawDataLoader, org_structure=FileOrgStructure.DATECOLUMN):
        t = time.perf_counter()
        self.name = name
        self.outputpath = OutputDataPath + "\\" + name + ".hdf5"
        self.referenceData = referenceData
        self.PVDataLoader = RawDataLoader
        self.org_structure = org_structure
        self.processed_halt_date = None
        self.processed_st_date = None
        self.processed_columns = set()

    def process(self, pv_data_processor, date, pv_data="1min_PV"):

        if self.processed_halt_date is None:
            self.processed_halt_date = self.process_halt_date()
            self.processed_st_date = self.process_st_date()

        t = time.perf_counter()
        pv_data = self.PVDataLoader.load_pv_data(pv_data, date, date)
        logger.debug(f"load_pv_data finished in {time.perf_counter() - t} seconds")
        processed_daily_pv = self.process_1min_pv_to_daily(pv_data_processor, pv_data)
        logger.debug(f"process_1min_pv_to_daily finished in {time.perf_counter() - t} seconds")
        processed_daily_pv = self.add_reference_data(processed_daily_pv, date)
        logger.debug(f"added all reference data in {time.perf_counter() - t} seconds")
        # processed_daily_pv.to_csv(self.outputpath.replace("hdf5", "csv"))
        self.write_data(date, processed_daily_pv, self.org_structure)
        logger.debug(f"wrote data in {time.perf_counter() - t} seconds")

    def load_processed(self, date, window, fields=None):
        output = []
        with h5py.File(self.outputpath, 'r') as f:
            dates = self.referenceData["Calendar"][["date", "is_open"]].astype(int)
            dates = dates[dates["is_open"] == 1]["date"].astype(str).values.tolist()
            dates = sorted(dates)
            index = dates.index(date)
            count = 0
            while count < window:
                curfiles = []
                curdate = dates[index + count]
                try:
                    curfile = f[curdate]
                    if fields is None:
                        fields = list(curfile)
                    for field in fields:
                        curfiles.append(pd.Series(curfile[field][:]).rename(field))
                    output.append(pd.concat(curfiles, axis=1))
                except:
                    logger.info(f"skipping loading on {curdate}")
                    pass
                count += 1
            f.close()
        return pd.concat(output).reset_index(drop=True)

    """ Helper Functions """

    def write_data(self, date, daily_df, org_structure):
        if org_structure is not FileOrgStructure.DATECOLUMN:
            raise Exception("Method not implemented")

        with h5py.File(self.outputpath, 'a') as f:
            dategroup = f.create_group(date)
            for column in daily_df.columns:
                try:
                    dategroup.create_dataset(column, data=daily_df[column].to_numpy())
                except:
                    dategroup.create_dataset(column, data=daily_df[column].to_numpy().astype(np.float64))
                    logger.info(f"forced conversion on {date} for {column}")
                self.processed_columns.add(column)
            f.close()

    @classmethod
    def write_data(cls, date, daily_df, org_structure, outputpath, name):
        if org_structure is not FileOrgStructure.DATECOLUMN:
            raise Exception("Method not implemented")

        with h5py.File(outputpath + r"/" + name + r"/" + date + ".hdf5", 'w') as f:
            for column in daily_df.columns:
                try:
                    f.create_dataset(column, data=daily_df[column].to_numpy())
                except:
                    f.create_dataset(column, data=daily_df[column].to_numpy().astype(np.float64))
            f.close()

    def process_halt_date(self):
        halt_date = self.referenceData["HaltDate"].copy()
        halt_date["restart_inclusive"] = halt_date.apply(lambda x: x["restart_time"] > 93000, axis=1)
        trade_date = self.referenceData["Calendar"].copy()
        trade_date = trade_date[trade_date["is_open"] == 1]

        output = []
        for row in halt_date.iterrows():
            code = row[1]["code"]
            halt_start = row[1]["halt_date"]
            restart_date = row[1]["restart_date"]
            if row[1]["restart_inclusive"]:
                tmp = trade_date[(trade_date["date"] >= halt_start) & (trade_date["date"] <= restart_date)].assign(
                    code=code).assign(is_halt=1)
            else:
                tmp = trade_date[(trade_date["date"] >= halt_start) & (trade_date["date"] < restart_date)].assign(
                    code=code).assign(is_halt=1)
            output.append(tmp[["code", "date", "is_halt"]])
        return pd.concat(output)

    def process_st_date(self):

        trade_date = self.referenceData["Calendar"].copy()
        trade_date_open = trade_date[trade_date["is_open"] == 1][["date", "is_open"]].set_index("date")
        trade_date_all = trade_date[["date", "is_open"]].set_index("date")

        st_status = self.referenceData["STDate"].copy()[["code", "status_id", "eff_date"]]
        st_status = st_status.pivot_table(index="eff_date", columns="code", values="status_id")
        st_status = trade_date_open.join(st_status).ffill().drop(columns="is_open")
        st_status = trade_date_all.join(st_status).drop(columns="is_open")
        st_status = st_status.stack().reset_index()
        st_status.columns = ["date", "code", "status_id"]
        st_status["date"] = st_status["date"].astype("int32")
        st_status["status_id"] = st_status["status_id"].astype("int32")
        return st_status

    def process_1min_pv_to_daily(self, pv_data_processor, pv_data):

        processed_1min_pv = pv_data_processor(pv_data)
        current_base = self.referenceData["ListDelistDate"].copy().set_index("code")
        joined_df = current_base.join(processed_1min_pv)
        return joined_df[processed_1min_pv.columns]

    def add_reference_data(self, processed_daily_pv, date):

        cumulative_adjustment_factor = self.referenceData["CumulativeAdjustmentFactor"][
            self.referenceData["CumulativeAdjustmentFactor"]["path"].apply(lambda x: date in x)].set_index("code")[
            ["cum_adjf"]]
        cumulative_adjustment_factor["cum_adjf"] = cumulative_adjustment_factor["cum_adjf"].astype(np.float64)

        halt_date = self.processed_halt_date.copy()
        halt_date = halt_date[halt_date["date"] == int(date)].set_index("code")[["is_halt"]]
        halt_date["is_halt"] = halt_date["is_halt"].astype(np.float64)

        current_status = self.referenceData["ListDelistDate"].copy()[
            ["code", "lst_status", "lst_date", "delst_date"]].set_index("code")
        current_status["lst_status"] = current_status["lst_status"].astype(np.string_)
        current_status["lst_date"] = current_status["lst_date"].astype(np.float64)
        current_status["delst_date"] = current_status["delst_date"].astype(np.float64)

        st_date = self.processed_st_date.copy()
        st_date = st_date[st_date["date"] == int(date)].set_index("code")[["status_id"]]
        st_date["status_id"] = st_date["status_id"].astype(np.float64)

        sector_classification = self.referenceData["Sector"][
            self.referenceData["Sector"]["path"].apply(lambda x: date in x)].set_index("code")[["sw1",
                                                                                                "sw2",
                                                                                                "sw3"]]

        limit_price = self.referenceData["LimitPrices"][
            self.referenceData["LimitPrices"]["path"].apply(lambda x: date in x)].set_index("code")[["up_limit",
                                                                                                     "down_limit"]]
        limit_price["up_limit"] = limit_price["up_limit"].astype(np.float64)
        limit_price["down_limit"] = limit_price["down_limit"].astype(np.float64)

        market_value = self.referenceData["MarketValue"][
            self.referenceData["MarketValue"]["path"].apply(lambda x: date in x)].set_index("code")[["neg_mkt_val",
                                                                                                     "mkt_val",
                                                                                                     "neg_shares",
                                                                                                     "shares"]]
        market_value["neg_mkt_val"] = market_value["neg_mkt_val"].astype(np.float64)
        market_value["mkt_val"] = market_value["mkt_val"].astype(np.float64)
        market_value["neg_shares"] = market_value["neg_shares"].astype(np.float64)
        market_value["shares"] = market_value["shares"].astype(np.float64)

        processed_daily_pv = processed_daily_pv.join(cumulative_adjustment_factor)
        processed_daily_pv = processed_daily_pv.join(halt_date)
        processed_daily_pv = processed_daily_pv.join(current_status)
        processed_daily_pv = processed_daily_pv.join(st_date)

        processed_daily_pv = processed_daily_pv.join(sector_classification)
        processed_daily_pv[["sw1", "sw2", "sw3"]] = processed_daily_pv[["sw1", "sw2", "sw3"]].fillna(value="")
        processed_daily_pv["sw1"] = processed_daily_pv["sw1"].str.encode('utf-8').astype(np.string_)
        processed_daily_pv["sw2"] = processed_daily_pv["sw2"].str.encode('utf-8').astype(np.string_)
        processed_daily_pv["sw3"] = processed_daily_pv["sw3"].str.encode('utf-8').astype(np.string_)

        processed_daily_pv = processed_daily_pv.join(limit_price)
        processed_daily_pv = processed_daily_pv.join(market_value)
        processed_daily_pv = processed_daily_pv.reset_index()
        processed_daily_pv["code"] = processed_daily_pv["code"].astype(np.string_)

        return processed_daily_pv
