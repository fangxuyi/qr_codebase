from data.dataloader import DataLoader
from data.dataprocessor import DataProcessor
import pandas as pd


class TestAlphaCalc:

    def __init__(self, alpha_name, universe, reference_data, parameter):
        self.alpha_name = alpha_name
        self.universe = universe
        self.parameter = parameter
        self.reference_data = reference_data
        self.data_loader = DataLoader(reference_data)

    def calculate(self, date):
        trade_dates = self.data_loader.get_all_trade_dates()
        universe = self.data_loader.get_current_universe(date, self.universe)["code"].to_list()
        try:
            idx = trade_dates.index(date)
            returns = self.data_loader.load_processed_window_list("pv_1min_return",
                                                                  trade_dates[idx - self.parameter["lookback"]:idx + 1])
            returns["code"] = returns["code"].apply(lambda x: x.decode('utf-8'))
            returns = returns.pivot_table(index="date", columns="code", values="return")
            returns = returns.reindex(universe, axis=1).dropna(how="any", axis=1)

            total_return = (returns + 1).prod() - 1
            total_return_avg = total_return.mean()
            total_return_sum = total_return.apply(lambda x: abs(x)).sum() / 2
            weight = (total_return - total_return_avg) / total_return_sum
            weight = pd.DataFrame(weight.rename("weight"))
            weight["date"] = date
            weight = weight.reset_index()
            DataProcessor.write_alpha_data(str(date), weight, self.alpha_name + "_" + self.universe)

        except:
            pass
