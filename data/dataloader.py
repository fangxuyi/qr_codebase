from .raw_data_loader_settings import OutputDataPath, AlphaOutputPath
import h5py
import logging
import pandas as pd

logger = logging.getLogger(__name__)

# TODO: add cache to data loader

class DataLoader:
    def __init__(self, referenceData):
        self.referenceData = referenceData
        self.trade_dates = self.get_all_trade_dates()

    def get_all_trade_dates(self):
        trade_date = self.referenceData["Calendar"][["date", "is_open"]].astype(int)
        trade_date = trade_date[(trade_date["is_open"] == 1)]["date"].tolist()
        trade_date = sorted(trade_date)
        return trade_date

    def load_processed_alpha_window_list(self, name, window_list, fields=None):
        output = []

        for date in window_list:
            try:
                with h5py.File(AlphaOutputPath + "\\" + name + "\\" + str(date) + ".hdf5", 'r') as f:
                    curfiles = []
                    if fields is None:
                        fields = list(f)
                    for field in fields:
                        curfiles.append(pd.Series(f[field][:]).rename(field))
                    f.close()
                output.append(pd.concat(curfiles, axis=1))
            except:
                logger.info(f"skipping loading on {date}")
                pass

        return pd.concat(output).reset_index(drop=True)

    def load_processed_window_list(self, name, window_list, fields=None):
        output = []
        with h5py.File(OutputDataPath + "\\" + name + ".hdf5", 'r') as f:
            for curdate in window_list:
                curfiles = []
                curdate = str(curdate)
                try:
                    curfile = f[curdate]
                    if fields is None:
                        fields = list(curfile)
                    for field in fields:
                        curfiles.append(pd.Series(curfile[field][:]).rename(field))
                    output.append(pd.concat(curfiles, axis=1).assign(date=curdate))
                except:
                    logger.info(f"skipping loading on {curdate}")
                    pass
            f.close()
        return pd.concat(output).reset_index(drop=True)

    def load_processed(self, date, name, window, fields=None):
        output = []
        with h5py.File(OutputDataPath + "\\" + name + ".hdf5", 'r') as f:
            index = self.trade_dates.index(date)
            count = 0
            while count < window:
                curfiles = []
                curdate = self.trade_dates[index + count]
                curdate = str(curdate)
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

    def get_halt_date(self):

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

    def get_trade_date_between(self, calc_start, calc_end):
        trade_date = self.referenceData["Calendar"][["date", "is_open"]].astype(int)
        trade_date = trade_date[(trade_date["is_open"] == 1) & (trade_date["date"] >= int(calc_start)) & (
                trade_date["date"] <= int(calc_end))]["date"].tolist()
        trade_date = sorted(trade_date)
        return trade_date

    def get_current_universe(self, date, universe):
        current_universe = self.referenceData[universe]
        current_universe = current_universe[current_universe["path"].apply(lambda x: str(date) in x)]["code"]
        return pd.DataFrame(current_universe)

    def get_adjustment_factor_window(self, date, window):
        output = []
        i = self.trade_dates.index(date)
        for idx in range(i, i + window):
            date = self.trade_dates[idx]
            tmp = self.get_adjustment_factor(date)
            tmp["date"] = date
            output.append(tmp)
        return pd.concat(output)

    def get_adjustment_factor(self, date):
        current_cumulative_adjustment_factor = self.referenceData["CumulativeAdjustmentFactor"]
        current_cumulative_adjustment_factor = \
            current_cumulative_adjustment_factor[
                current_cumulative_adjustment_factor["path"].apply(lambda x: str(date) in x)][
                "code"]
        return pd.DataFrame(current_cumulative_adjustment_factor)
