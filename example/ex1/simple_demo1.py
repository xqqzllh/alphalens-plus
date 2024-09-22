from gquant import *
import pandas as pd
import alphalens
import csv

def read_csv_to_dict(file_path):
    result_dict = {}
    with open(file_path, mode='r', encoding='utf-8') as file:
        csv_reader = csv.reader(file)
        for row in csv_reader:
            if len(row) >= 2:  # 确保每行至少有两列
                key = row[0]
                value = row[1]
                result_dict[key] = value
    return result_dict


stock_2_idx = read_csv_to_dict("../example-data/stock_2_idx.csv")
idx_2_name = read_csv_to_dict("../example-data/idx_2_name.csv")

# #加载数据
factors = pd.read_csv('../example-data/factor.csv', parse_dates=True, index_col=['date', 'asset'])
prices = pd.read_csv('../example-data/prices.csv', parse_dates=True, index_col=['date'])

return_data = alphalens.utils.get_clean_factor_and_forward_returns(factors, prices, quantiles=10, groupby=stock_2_idx,
                                                                   groupby_labels=idx_2_name, periods=(1, 5, 20))
alphalens.tears.create_summary_tear_sheet(return_data)

# 生成分析图
alphalens.tears.create_full_tear_sheet(return_data)
