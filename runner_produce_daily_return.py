from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
from data.raw_data_loader_settings import FileOrgStructure
from data.rawdataloader import RawDataLoader
import logging

if __name__ == '__main__':

    logger = logging.getLogger(__name__)
    logging.basicConfig(level=logging.INFO)

    # load processed
    calc_start = "20180101"
    calc_end = "20201231"

    referenceData = RawDataLoader.load_all_reference_data()
    dataLoader = DataLoader(referenceData)
    all_dates_to_process = dataLoader.get_trade_date_between(calc_start, calc_end)
    processed_daily = dataLoader.load_processed_window_list("pv_1min_standard", all_dates_to_process, ["code", "close", "cum_adjf"])

    # calculate 1min return
    processed_daily = processed_daily.pivot_table(index="date", columns="code", values="close")
    processed_daily_adjf = processed_daily.pivot_table(index="date", columns="code", values="cum_adjf")
    processed_daily = processed_daily * processed_daily_adjf
    processed_daily = processed_daily.diff() / processed_daily.shift()
    processed_daily = processed_daily.unstack().rename("return").reset_index().dropna()

    dataProcessor = DataProcessor("pv_1min_return", referenceData, RawDataLoader)
    dates = processed_daily["date"].drop_duplicates()
    for date in dates:
        daily_df = processed_daily[processed_daily["date"] == date]
        dataProcessor.write_data(date, daily_df, FileOrgStructure.DATECOLUMN)

    processed_daily_return = dataLoader.load_processed_window_list("pv_1min_return", all_dates_to_process)
