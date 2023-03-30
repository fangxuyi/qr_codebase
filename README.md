example:

referenceData = RawDataLoader.load_all_reference_data()
dataProcessor = DataProcessor(name, referenceData, RawDataLoader)
dataProcessor.process(pv_data_processor, date, pv_data="1min_PV") -> data_processor
dataProcessor.load_processed(date, window, fields=None) -> data_loader
