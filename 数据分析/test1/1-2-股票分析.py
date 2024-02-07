# 第一步
# -*- coding: utf-8 -*-
# 导入numpy库，并命名为np
import numpy as np

# 第二步
# dict() 函数用于创建一个字典数据:dic_data1
dic_data1 = dict(
    # fname表示读取的文件
    fname="股票分析数据.csv",
    # delimiter表示数据分隔符
    delimiter=',',
    # usecols表示读取的列坐标
    usecols=(2, 3, 4, 5, 6),
    # skiprows跳过前x行，1表示跳过第一行表头
    skiprows=1,
    # encoding = 'utf-8'表示使用指定的字符集打开文件
    encoding='utf-8',
    # unpack表示如果为True,读入属性将分别写入不同数组变量，False读入数据只写入一个数组变量，默认False
    unpack=True
)

# 第三步
# 使用np.loadtxt方法读取字典dic_data1，并将指定列的数据分别赋值给col2,col3,col4,col5,col6
col2, col3, col4, col5, col6 = np.loadtxt(**dic_data1)
# 输出收盘价
print("收盘价=", col5)
# 输出交易额
print("交易额=", col6)

# 第四步
# 使用np.average方法计算平均价和加权平均价
col5_average = np.average(col5)
col6_wave = np.average(col5, weights=col6)
print("平均价=", col5_average)
print("加权平均价=", col6_wave)

# 第五步
# 使用np.max和np.min方法计算最高价和最低价
col3_maxPrice = np.max(col3)
col4_minPrice = np.min(col4)
print("最高价=", col3_maxPrice)
print("最低价=", col4_minPrice)

# 第六步
# 使用np.ptp方法计算最高差价和最低差价
col3_highvalue = np.ptp(col3)
col4_lowvalue = np.ptp(col4)
print("最高差价=", col3_highvalue)
print("最低差价=", col4_lowvalue)

# 第七步
# 使用np.median方法计算盘价的中位数
col2_midPrice = np.median(col2)
print("开盘价的中位数=", col2_midPrice)
# 使用np.var计算开盘价的方差
col2_var = np.var(col2)
print("开盘价的方差=", col2_var)

# 第八步
# 使用np.diff方法计算对数收益率
col5_logearning = np.diff(np.log(col5))
# 使用std()函数计算方差，mean()函数计算均值，sqrt()函数计算平方根
col5_year_volatility = col5_logearning.std() / col5_logearning.mean() * np.sqrt(252)
col5_month_volatility = col5_logearning.std() / col5_logearning.mean() * np.sqrt(12)
# 输出年波动率和月波动率
print("年波动率=", col5_year_volatility)
print("月波动率=", col5_month_volatility)
