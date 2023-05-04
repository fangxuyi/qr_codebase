import yaml
from calcutil.alpha_calc_config import ConfigPath


if __name__ == '__main__':
    alpha_calculator_cfg_dict = {
        "momentum_3_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
            }
        },
        "momentum_5_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
            }
        },
        "momentum_10_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_close.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "open_to_close_momentum_w_volume_3_ZZ9999": {
            "classname": "Price.OpenToCloseMomentumWithVolumeFilter",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
            }
        },
        "open_to_close_momentum_w_volume_5_ZZ9999": {
            "classname": "Price.OpenToCloseMomentumWithVolumeFilter",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
            }
        },
        "open_to_close_momentum_w_volume_10_ZZ9999": {
            "classname": "Price.OpenToCloseMomentumWithVolumeFilter",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_opentoclose_with_volume.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "open_to_close_momentum_w_volume_corr_7_ZZ9999": {
            "classname": "Price.OpenToCloseMomentumWithVolumeCorr",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 7,
            }
        },
        "open_to_close_momentum_w_volume_corr_15_ZZ9999": {
            "classname": "Price.OpenToCloseMomentumWithVolumeCorr",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 15,
            }
        },
        "open_to_close_momentum_w_volume_corr_21_ZZ9999": {
            "classname": "Price.OpenToCloseMomentumWithVolumeCorr",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 21,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_opentoclose_with_volume_correlation.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "open_to_close_reversal_3_ZZ9999": {
            "classname": "Price.OpenToCloseReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
            }
        },
        "open_to_close_reversal_5_ZZ9999": {
            "classname": "Price.OpenToCloseReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
            }
        },
        "open_to_close_reversal_10_ZZ9999": {
            "classname": "Price.OpenToCloseReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },
        "open_to_close_reversal_21_ZZ9999": {
            "classname": "Price.OpenToCloseReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 21,
            }
        },
        "open_to_close_reversal_63_ZZ9999": {
            "classname": "Price.OpenToCloseReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 63,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_opentoclose_with_volume_correlation.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "open_to_close_momentum_3_ZZ9999": {
            "classname": "Price.OpenToCloseMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
            }
        },
        "open_to_close_momentum_5_ZZ9999": {
            "classname": "Price.OpenToCloseMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
            }
        },
        "open_to_close_momentum_10_ZZ9999": {
            "classname": "Price.OpenToCloseMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_opentoclose.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "reversal_10_ZZ9999": {
            "classname": "Price.Reversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },
        "reversal_21_ZZ9999": {
            "classname": "Price.Reversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 21,
            }
        },
        "reversal_63_ZZ9999": {
            "classname": "Price.Reversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 63,
            }
        },}
    file = open(ConfigPath + r"\daily\reversal_close.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "gapped_reversal_63_ZZ9999": {
            "classname": "Price.GappedReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackstart": 21,
                "lookbackend": 63,
            }
        },
        "gapped_reversal_21_ZZ9999": {
            "classname": "Price.GappedReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackstart": 5,
                "lookbackend": 21,
            }
        },
        "gapped_reversal_10_ZZ9999": {
            "classname": "Price.GappedReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackstart": 3,
                "lookbackend": 10,
            }
        },}
    file = open(ConfigPath + r"\daily\reversal_gapped_close.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "ts_momentum_3_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
            }
        },
        "ts_momentum_5_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
            }
        },
        "ts_momentum_10_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_ts_close.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "momentum_change_3_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
                "gap": 1,
            }
        },
        "momentum_change_5_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
                "gap": 3,
            }
        },
        "momentum_change_10_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
                "gap": 5,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_change_close.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "max_ratio_3_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
            }
        },
        "max_ratio_5_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
            }
        },
        "max_ratio_10_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_max_ratio.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "binary_count_3_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
            }
        },
        "binary_count_5_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
            }
        },
        "binary_count_10_ZZ9999": {
            "classname": "Price.Momentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_binary_count_close.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "vol_adj_momentum_3_ZZ9999": {
            "classname": "Price.VolAdjMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackwindow": 3,
                "volwindow": 21,
            }
        },
        "vol_adj_momentum_5_ZZ9999": {
            "classname": "Price.VolAdjMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackwindow": 5,
                "volwindow": 21,
            }
        },
        "vol_adj_momentum_10_ZZ9999": {
            "classname": "Price.VolAdjMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackwindow": 10,
                "volwindow": 21,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_vol_adj_return_close.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "vol_adj_ts_momentum_3_ZZ9999": {
            "classname": "Price.VolAdjTSMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackwindow": 3,
                "volwindow": 21,
            }
        },
        "vol_adj_ts_momentum_5_ZZ9999": {
            "classname": "Price.VolAdjTSMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackwindow": 5,
                "volwindow": 21,
            }
        },
        "vol_adj_ts_momentum_10_ZZ9999": {
            "classname": "Price.VolAdjTSMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackwindow": 10,
                "volwindow": 21,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_vol_adj_ts_close.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "ewma_adj_momentum_3_ZZ9999": {
            "classname": "Price.EWMAAdjMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackwindow": 3,
                "span": 3,
            }
        },
        "ewma_adj_momentum_5_ZZ9999": {
            "classname": "Price.EWMAAdjMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackwindow": 5,
                "span": 3,
            }
        },
        "ewma_adj_momentum_10_ZZ9999": {
            "classname": "Price.EWMAAdjMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookbackwindow": 10,
                "span": 3,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_ewma_adj_close.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "expanded_ts_momentum_3_ZZ9999": {
            "classname": "Price.ExpandedTimeSeriesMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 21,
                "shortwindow": 3,
            }
        },
        "expanded_ts_momentum_5_ZZ9999": {
            "classname": "Price.ExpandedTimeSeriesMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 21,
                "shortwindow": 5,
            }
        },
        "expanded_ts_momentum_10_ZZ9999": {
            "classname": "Price.ExpandedTimeSeriesMomentum",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 21,
                "shortwindow": 10,
            }
        },}
    file = open(ConfigPath + r"\daily\momentum_expanded_close.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "intraday_consistency_1_ZZ9999": {
            "classname": "Price.ConsistencyInIntradayPriceMovement",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 1,
            }
        },
        "intraday_consistency_2_ZZ9999": {
            "classname": "Price.ConsistencyInIntradayPriceMovement",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 2,
            }
        },
        "intraday_consistency_3_ZZ9999": {
            "classname": "Price.ConsistencyInIntradayPriceMovement",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
            }
        },
        "intraday_consistency_5_ZZ9999": {
            "classname": "Price.ConsistencyInIntradayPriceMovement",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
            }
        },
        "intraday_consistency_10_ZZ9999": {
            "classname": "Price.ConsistencyInIntradayPriceMovement",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },
        "intraday_consistency_21_ZZ9999": {
            "classname": "Price.ConsistencyInIntradayPriceMovement",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 21,
            }
        },
        "intraday_consistency_63_ZZ9999": {
            "classname": "Price.ConsistencyInIntradayPriceMovement",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 63,
            }
        },}
    file = open(ConfigPath + r"\intraday\reversal_consistency_in_movement.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "top_bottom_return_reversal_1_ZZ9999": {
            "classname": "Price.TopBottomTradeReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 1,
            }
        },
        "top_bottom_return_reversal_2_ZZ9999": {
            "classname": "Price.TopBottomTradeReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 2,
            }
        },
        "top_bottom_return_reversal_3_ZZ9999": {
            "classname": "Price.TopBottomTradeReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
            }
        },
        "top_bottom_return_reversal_5_ZZ9999": {
            "classname": "Price.TopBottomTradeReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
            }
        },
        "top_bottom_return_reversal_10_ZZ9999": {
            "classname": "Price.TopBottomTradeReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },

        "top_bottom_return_reversal_21_ZZ9999": {
            "classname": "Price.TopBottomTradeReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 21,
            }
        },
        "top_bottom_return_reversal_63_ZZ9999": {
            "classname": "Price.TopBottomTradeReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 63,
            }
        },}
    file = open(ConfigPath + r"\intraday\top_to_bottom_return.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()

    alpha_calculator_cfg_dict = {
        "ranked_short_term_low_reserval_3_ZZ9999": {
            "classname": "Price.ShortTermLowReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 3,
            }
        },
        "ranked_short_term_low_reserval_5_ZZ9999": {
            "classname": "Price.ShortTermLowReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 5,
            }
        },
        "ranked_short_term_low_reserval_10_ZZ9999": {
            "classname": "Price.ShortTermLowReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 10,
            }
        },

        "ranked_short_term_low_reserval_21_ZZ9999": {
            "classname": "Price.ShortTermLowReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 21,
            }
        },
        "ranked_short_term_low_reserval_63_ZZ9999": {
            "classname": "Price.ShortTermLowReversal",
            "universe": "ZZ9999",
            "parameters": {
                "lookback": 63,
            }
        },
    }
    file = open(ConfigPath + r"\daily\reversal_ranked_short_term_low.yaml", "w")
    yaml.dump(alpha_calculator_cfg_dict, file)
    file.close()