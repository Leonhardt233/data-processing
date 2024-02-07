# 第一步
# -*- coding: utf-8 -*-
# 导入numpy库，并命名为np
import numpy as np

# 第二步
# dict() 函数用于创建一个字典数据:dic_data1
dic_data1 = dict(
    # fname表示读取的文件
    fname = "电影数据.csv",
    # delimiter表示数据分隔符
    delimiter = ',',
    # usecols表示读取的列坐标
    usecols = (2,6,8),
    # skiprows跳过前x行，1表示跳过第一行表头
    skiprows = 1,
    # encoding = 'utf-8'表示使用指定的字符集打开文件
    encoding = 'utf-8',
    # unpack表示如果为True,读入属性将分别写入不同数组变量，False读入数据只写入一个数组变量，默认False
    unpack = True
    )

# 第三步
# 使用np.loadtxt方法读取字典dic_data1，并将指定列的数据统一赋值给a，组成一个新的ndarray数组。
a = np.loadtxt(**dic_data1)
# 通过a的数组下标分别获取指定的字段数据：投票数量、电影时长、电影评分
# print("投票数量=",a[0])
# print("电影时长=",a[1])
# print("电影评分=",a[2])

# 第四步
# dict() 函数用于创建一个字典数据:dic_data2
dic_data2 = dict(
    # fname表示读取的文件
    fname = "电影数据.csv",
    # delimiter表示数据分隔符
    delimiter = ',',
    # dtype表示输出的源数据类型
    dtype = str,
    # usecols表示读取的列坐标
    usecols = (1),
    # skiprows跳过前x行，1表示跳过第一行表头
    skiprows = 1,
    # encoding = 'utf-8'表示使用指定的字符集打开文件
    encoding = 'utf-8',
    # unpack表示如果为True,读入属性将分别写入不同数组变量，False读入数据只写入一个数组变量，默认False
    unpack = True
    )

# 第五步
# 使用np.loadtxt方法读取字典dic_data2，并将指定列的数据统一赋值给b，组成一个新的ndarray数组。
b = np.loadtxt(**dic_data2)
# 通过a的数组下标分别获取指定的字段数据：电影名称
# print("电影名称=",b[0:10])

# 第六步
# 使用np.max和np.min方法计算最高评分、最低评分，平均评分、最高投票数量、最低投票数量、最长电影时长、最短电影时长
a0_maxVote = np.max(a[0])
a0_minVote = np.min(a[0])
a1_maxLength = np.max(a[1])
a1_minLength = np.min(a[1])
a2_maxScore = np.max(a[2])
a2_minScore = np.min(a[2])
a2_avgScore = np.average(a[2])
print("最高投票数量=",a0_maxVote)
print("最低投票数量=",a0_minVote)
print("最长电影时长=",a1_maxLength)
print("最短电影时长=",a1_minLength)
print("最高评分=",a2_maxScore)
print("最低评分=",a2_minScore)
print("平均评分=",a2_avgScore)

# 第七步
# 获取评分最高和最低的电影名称
a2_max_lst = []
a2_min_lst = []
for i in range(len(a[2])):
    if (a[2][i] == 9.6):
        a2_max_lst.append(b[i])
    elif (a[2][i] == 2.6):
        a2_min_lst.append(b[i])
print("最高评分电影名称：",a2_max_lst)
print("最低评分电影名称：",a2_min_lst)

# 第八步
# 获取时长最长和最短的电影
a1_max_lst = []
a1_min_lst = []
for i in range(len(a[1])):
    if (a[1][i] == 366.0):
        a1_max_lst.append(b[i])
    elif (a[1][i] == 3.0):
        a1_min_lst.append(b[i])
print("时长最长的电影名称：",a1_max_lst)
print("时长最短的电影名称：",a1_min_lst)

# 第九步
# 获取投票数最多和最少的电影
a0_max_lst = []
a0_min_lst = []
for i in range(len(a[0])):
    if (a[0][i] == 692795.0):
        a0_max_lst.append(b[i])
    elif (a[0][i] == 28.0):
        a0_min_lst.append(b[i])
print("时长最长的电影名称：",a0_max_lst)
print("时长最短的电影名称：",a0_min_lst)