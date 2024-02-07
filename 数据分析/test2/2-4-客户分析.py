# 查看数据
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl

# 使用read_csv函数读取文件
df_data = pd.read_csv('./dataset.csv', encoding='utf-8')
# 查看数据前5行
print(df_data.head())
# 查看数据基本信息
# df_data.info()
# 查看数据维度
print(df_data.shape)
# #非空统计
print(df_data.count())
# 统计数据空值数量
print(df_data.isnull().sum())
# 查看描述统计信息
print(df_data.describe())
# 清洗数据
# 将其转化成时间（发货时间，下单日期均为object，需要先转化成时间）
df_data['发货时间'] = pd.to_datetime(df_data['发货时间'])
df_data['下单日期'] = pd.to_datetime(df_data['下单日期'])
# 查看数据基本信息
df_data.info()

# 删去发货时间早于下单日期的记录，且在原数据上进行修改
df_data.drop(index=df_data[df_data['发货时间'] < df_data['下单日期']].index, inplace=True)

# 删去序号重复的记录，且在原数据上进行修改
df_data.drop(index=df_data[df_data.序号.duplicated()].index, inplace=True)
# 查看发货模式空值
print(df_data[df_data.发货模式.isnull()]['发货模式'])
# 对空值进行修补
# 从选择的某个轴 返回这个众数, 如果缺失就是用NaN填充, 然后  轴上可能会有多个众数,所以这个函数返回的类型是一个dateframe
print(df_data.发货模式.mode()[0])
# 进行空值填充
df_data['发货模式'].fillna(value=df_data.发货模式.mode()[0], inplace=True)
# df_data.info()
# 分别取出订单日期的年、月、季
df_data['下单年份'] = df_data['下单日期'].dt.year
df_data['下单月份'] = df_data['下单日期'].dt.month
df_data['下单季度'] = df_data['下单日期'].dt.to_period('Q')
# result = df_data [['下单日期','下单年份','下单月份', '下单季度']].head()
# print(result)
# 获取每年的销售总金额
year_sale = df_data.groupby(by='下单年份')['购买价格'].sum()
print(year_sale)
# 获取每年的利润总金额
sale_pf = df_data.groupby(by='下单年份')['利润'].sum()
print(sale_pf)
# 获取每年的总邮寄费用
sale_shipcost = df_data.groupby(by='下单年份')['邮费'].sum()
print(sale_shipcost)
# 获取每年的销售总数
sale_qt = df_data.groupby(by='下单年份')['购买数量'].sum()
print(sale_qt)

# 设置字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
# 设置风格
plt.style.use('ggplot')
# 以折线图呈现每年销售总金额变化
year_sale = df_data.groupby(by='下单年份')['购买价格'].sum()
# plt.plot(year_sale.index, year_sale)

# 以饼图图呈现每年利润总金额变化
sale_pf = df_data.groupby(by='下单年份')['利润'].sum()
explode = (0, 0.1, 0, 0)
labels = sale_pf.index
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
# plt.pie(sale_pf, explode=explode, labels=labels, colors=colors, autopct='%1.1f%%', shadow=True,startangle=90)

# 以直方图呈现每年邮费总金额变化
sale_shipcost = df_data.groupby(by='下单年份')['邮费'].sum()
plt.bar(sale_shipcost.index, sale_shipcost, align='center', color='b')
# 分别取出订单日期的年、月、季
df_data['下单年份'] = df_data['下单日期'].dt.year
df_data['下单月份'] = df_data['下单日期'].dt.month
df_data['下单季度'] = df_data['下单日期'].dt.to_period('Q')
# result = df_data [['下单日期','下单年份','下单月份', '下单季度']].head()
# print(result)
# 获取每年的销售利润总金额
year_sale = df_data.groupby(by='下单年份')['利润'].sum()
# 利润增长率 = 本年的利润/上年的利润 - 1
rate_2018 = year_sale[2018] / year_sale[2017] - 1
rate_2019 = year_sale[2019] / year_sale[2018] - 1
rate_2020 = year_sale[2020] / year_sale[2019] - 1
# print(rate_2018,rate_2019,rate_2020)
# 转换利润增长率为浮点型数据，保留两位小数点。
rate_2018_label = "%.2f%%" % (rate_2018 * 100)
rate_2019_label = "%.2f%%" % (rate_2019 * 100)
rate_2020_label = "%.2f%%" % (rate_2020 * 100)
print(rate_2018_label, rate_2019_label, rate_2020_label)

# 设置字体
mpl.rcParams['font.sans-serif'] = ['SimHei']
mpl.rcParams['axes.unicode_minus'] = False
# 设置风格
plt.style.use('ggplot')
# 使用DataFrame创建DataFrame对象，并传入指定的列：sales_profit，sales_rate和sales_rate_label，及其对应的值。
sale_rate = pd.DataFrame(
    {'sale_pf': year_sale,
     'sale_rate': [0, rate_2018, rate_2019, rate_2020],
     'rate_label': ['0.00%', rate_2018_label, rate_2019_label, rate_2020_label]
     })
# 给可视化组合图准备数据，y1和y2分别给条形图和折线图的Y轴赋值。
y1 = sale_rate['sale_pf']
y2 = sale_rate['sale_rate']
# 通过for循环获得sales_rate.index的年份
x = [str(value) for value in sale_rate.index.tolist()]
# 新建figure对象
fig = plt.figure()
# 新建子图1
ax1 = fig.add_subplot(1, 1, 1)

# ax2与ax1共享X轴
ax2 = ax1.twinx()
# 绘制条形图
ax1.bar(x, y1, color='r')
# 绘制折线图
ax2.plot(x, y2, marker='*', color='b')
# 设置条形图和折线图标签和标题
ax1.set_xlabel('年份')
ax1.set_ylabel('净值')
ax2.set_ylabel('增长率')
ax1.set_title('净值与增长率')
plt.show()

# 不同交易地区区域的邮费总额
region = df_data.groupby(by='交易地区')['邮费'].sum()
region.plot(kind='pie')
region.plot(kind='pie', autopct="%1.2f%%", title='不同区域的邮费价格')
plt.show()
# 各地区每一年的销售数量
area = df_data.groupby(by=['交易地区', '下单年份'], as_index=False)['购买数量'].sum()
# area

# 使用数据透视表重新整理数据
area = pd.pivot_table(area,
                      index='交易地区',
                      columns='下单年份',
                      values='购买数量')

# 绘制图形
colors = ['yellowgreen', 'gold', 'lightskyblue', 'lightcoral']
area.plot(kind='bar', title='各地区2017到2020年的销售数量', color=colors)
# 取出订单日期为2018年的数据
data_2018 = df_data[df_data['下单年份'] == 2018]
# 取出三列
data_2018 = data_2018[['顾客ID', '下单日期', '购买价格']]
# 重新复制给df_custom
df_custom = data_2018.copy()
# 设置df_custom的索引为顾客ID，drop=True就是把原来的索引index列去掉，重置index，inplace=True表示直接在原数组上对数据进行修改。
df_custom.set_index('顾客ID', drop=True, inplace=True)
# 增加一个辅助列，每一条订单都计数为1
df_custom['订单'] = 1
# df_custom
# 透视图index为索引，values为列名，aggfunc操作函数
df_rfm = df_custom.pivot_table(index=['顾客ID'],
                               values=['下单日期', '订单', '购买价格'],
                               aggfunc={'下单日期': 'max',
                                        '订单': 'sum',
                                        '购买价格': 'sum'})

# 计算用户最后一次购买时间和第一次购买时间间隔，并添加到新增列：R
df_rfm['R'] = (df_rfm.下单日期.max() - df_rfm.下单日期).dt.days
# df_rfm
# 重命名'购买价格':'M','订单':'F'
df_rfm.rename(columns={'购买价格': 'M', '订单': 'F'}, inplace=True)


# 自定义函数rfm_func用于给不同的客户进行编码。分别计算'下单日期'、'购买价格'和'订单'字段与各自的平均值相减的结果（正数表示1，负数表示0）
def rfm_func(x):
    #     -25.0	7.0	1969.12304
    #      0     1     1
    level = x.apply(lambda x: "1" if x >= 0 else '0')

    #     0     1     1  -> 011
    label = level.R + level.F + level.M

    d = {
        '011': '重要价值客户',
        '111': '重要唤回客户',
        '001': '重要深耕客户',
        '101': '重要挽留客户',
        '010': '潜力客户',
        '110': '一般维持客户',
        '000': '新客户',
        '100': '流失客户'
    }
    result = d[label]
    return result


# 使用'R','F','M'与各自的平均值相减的方法，判断其客户重要程度
result1 = df_rfm[['R', 'F', 'M']].apply(lambda x: x - x.mean())
# 根据'R','F','M'与各自的平均值相减的结果，对不同的客户进行分类
# result2 = result1.apply(rfm_func,axis=1)
# result2
# 将客户分类的结果添加到rfmdf中，增加新的列：labels
# df_rfm['labels'] = result2
# df_rfm
