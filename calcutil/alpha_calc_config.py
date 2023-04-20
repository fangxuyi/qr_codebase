pool_size = 16

calc_start = "20180601"
calc_end = "20201231"

universe_options = [
    "HS300", "ZZ500", "ZZ800", "ZZ1000", "ZZ9999"
]

alpha_calculator_cfg_dict = {
    "momentum_3": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 3,
        }
    },
    "momentum_5": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 5,
        }
    },
    "momentum_10": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 10,
        }
    },
    "reversal_10": {
        "classname": "Price.Reversal",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 10,
        }
    },
    "reversal_21": {
        "classname": "Price.Reversal",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 21,
        }
    },
    "reversal_63": {
        "classname": "Price.Reversal",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 63,
        }
    },
    "gapped_reversal_63": {
        "classname": "Price.Reversal",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackstart": 21,
            "lookbackend": 63,
        }
    },
    "gapped_reversal_21": {
        "classname": "Price.Reversal",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackstart": 5,
            "lookbackend": 21,
        }
    },
    "gapped_reversal_10": {
        "classname": "Price.Reversal",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackstart": 3,
            "lookbackend": 10,
        }
    },
    "ts_momentum_3": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 3,
        }
    },
    "ts_momentum_5": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 5,
        }
    },
    "ts_momentum_10": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 10,
        }
    },
    "momentum_change_3": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 3,
            "gap": 1,
        }
    },
    "momentum_change_5": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 5,
            "gap": 3,
        }
    },
    "momentum_change_10": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 10,
            "gap": 5,
        }
    },
    "max_ratio_3": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 3,
        }
    },
    "max_ratio_5": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 5,
        }
    },
    "max_ratio_10": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 10,
        }
    },
    "binary_count_3": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 3,
        }
    },
    "binary_count_5": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 5,
        }
    },
    "binary_count_10": {
        "classname": "Price.Momentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 10,
        }
    },
    "vol_adj_momentum_3": {
        "classname": "Price.VolAdjMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackwindow": 3,
            "volwindow": 21,
        }
    },
    "vol_adj_momentum_5": {
        "classname": "Price.VolAdjMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackwindow": 5,
            "volwindow": 21,
        }
    },
    "vol_adj_momentum_10": {
        "classname": "Price.VolAdjMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackwindow": 10,
            "volwindow": 21,
        }
    },
    "vol_adj_ts_momentum_3": {
        "classname": "Price.VolAdjTSMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackwindow": 3,
            "volwindow": 21,
        }
    },
    "vol_adj_ts_momentum_5": {
        "classname": "Price.VolAdjTSMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackwindow": 5,
            "volwindow": 21,
        }
    },
    "vol_adj_ts_momentum_10": {
        "classname": "Price.VolAdjTSMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackwindow": 10,
            "volwindow": 21,
        }
    },
    "ewma_adj_momentum_3": {
        "classname": "Price.EWMAAdjMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackwindow": 3,
            "span": 3,
        }
    },
    "ewma_adj_momentum_5": {
        "classname": "Price.EWMAAdjMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackwindow": 5,
            "span": 3,
        }
    },
    "ewma_adj_momentum_10": {
        "classname": "Price.EWMAAdjMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookbackwindow": 10,
            "span": 3,
        }
    },
    "expanded_ts_momentum_3": {
        "classname": "Price.ExpandedTimeSeriesMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 21,
            "shortwindow": 3,
        }
    },
    "expanded_ts_momentum_5": {
        "classname": "Price.ExpandedTimeSeriesMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 21,
            "shortwindow": 5,
        }
    },
    "expanded_ts_momentum_10": {
        "classname": "Price.ExpandedTimeSeriesMomentum",
        "universe": "ZZ9999",
        "parameters": {
            "lookback": 21,
            "shortwindow": 10,
        }
    },
}

# TODO: yaml file for config

