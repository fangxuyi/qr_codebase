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

    def calculate(self, date, trade_dates):
        current_universe = self.data_loader.get_current_universe(self, date, self.universe)
        adj_factor = self.data_loader.get_adjustment_factor(date, 5, trade_dates)
        prices = self.dataloader.load_processed(date, "1min_PV", 5, trade_dates)

        result = pd.DataFrame()
        print(f"calculating {self.name} with parameter {self.parameter}")
        DataProcessor.write_alpha_data(date, result, self.alpha_name + "_" + self.universe)
