# example

#### referenceData = RawDataLoader.load_all_reference_data()
#### dataProcessor = DataProcessor(name, referenceData, RawDataLoader)
#### case 1: dataProcessor.process(pv_data_processor, date, pv_data="1min_PV") -> data_processor
#### case 2: dataProcessor.load_processed(date, window, fields=None) -> data_loader
