from dataloader import DataLoader
from dataprocessor import DataProcessor
from settings import FileOrgStructure, AlphaOutputPath
import pandas as pd


class TestAlphaCalc:
    output_path = AlphaOutputPath
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
        DataProcessor.write_data(date, result, FileOrgStructure.DATECOLUMN, TestAlphaCalc.output_path, self.alpha_name)
