from settings import OutputDataPath
import h5py
import logging
import pandas as pd

logger = logging.getLogger(__name__)


class DataLoader:
    def __init__(self, referenceData):
        self.referenceData = referenceData
        self.trade_dates = self.get_all_trade_dates()

    def get_all_trade_dates(self):
        trade_date = self.referenceData["Calendar"][["date", "is_open"]].astype(int)
        trade_date = trade_date[(trade_date["is_open"] == 1)]["date"].tolist()
        trade_date = sorted(trade_date)
        return trade_date

    def load_processed(self, date, name, window, fields=None):
        output = []
        with h5py.File(OutputDataPath + "\\" + name + ".hdf5", 'r') as f:
            index = self.trade_dates.index(date)
            count = 0
            while count < window:
                curfiles = []
                curdate = self.trade_dates[index + count]
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

    def get_trade_date_between(self, calc_start, calc_end):
        trade_date = self.referenceData["Calendar"][["date", "is_open"]].astype(int)
        trade_date = trade_date[(trade_date["is_open"] == 1) & (trade_date["date"] >= int(calc_start)) & (
                trade_date["date"] <= int(calc_end))]["date"].tolist()
        trade_date = sorted(trade_date)
        return trade_date

    def get_current_universe(self, date, universe):
        current_universe = self.reference_data[universe]
        current_universe = current_universe[current_universe["path"].apply(lambda x: date in x)]["code"].tolist()
        return current_universe

    def get_adjustment_factor(self, date, window):
        output = []
        i = self.trade_dates.index(date)
        for idx in range(i, window):
            date = self.trade_dates[idx]
            tmp = self.get_adjustment_factor(date)
            tmp["date"] = date
            output.append(tmp)
        return pd.concat(output)

    def get_adjustment_factor(self, date):
        current_cumulative_adjustment_factor = self.reference_data["CumulativeAdjustmentFactor"]
        current_cumulative_adjustment_factor = \
        current_cumulative_adjustment_factor[current_cumulative_adjustment_factor["path"].apply(lambda x: date in x)][
            "code"].tolist()
        return current_cumulative_adjustment_factor