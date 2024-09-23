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


# 1、读入板块信息
stock_2_idx = read_csv_to_dict("../example-data/stock_2_idx.csv")

idx_2_name = read_csv_to_dict("../example-data/idx_2_name.csv")

# 2、读入因子信息
factors = pd.read_csv('../example-data/factor.csv', parse_dates=True, index_col=['date', 'asset'])

# 3、读入价格信息
prices = pd.read_csv('../example-data/prices.csv', parse_dates=True, index_col=['date'])

# 这个地方需要把第二层的标的名转换一下类型,标的统一用string类型
factors.index = factors.index.set_levels(factors.index.levels[1].astype(str), level=1)

# 4、因子和价格信息整合到一个单一表
return_data = alphalens.utils.get_clean_factor_and_forward_returns(factors, prices, quantiles=10, groupby=stock_2_idx,
                                                                   groupby_labels=idx_2_name, periods=(1, 5, 20))

# 5、因子综合分析
alphalens.tears.create_summary_tear_sheet(return_data)

# 6、因子全面分析
alphalens.tears.create_full_tear_sheet(return_data)
