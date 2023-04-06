pool_size = 16

calc_start = "20180101"
calc_end = "20201231"

universe_options = [
    "HS300", "ZZ500", "ZZ800", "ZZ1000", "ZZ9999"
]

alpha_calculator_cfg_dict = {
    "alpha_algo_1": {
        "classname": "TestAlpha.TestAlphaCalc",
        "universe": "ZZ9999",
        "parameters": {
            "params1": 1,
            "params2": 1,
        }
    }
}

alpha_perfmc_cfg_list = ["alpha_algo_1"]