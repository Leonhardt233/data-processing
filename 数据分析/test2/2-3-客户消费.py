import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl

# 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体['KaiTi', 'SimHei', 'FangSong']
mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']
# # 字符集选择
# #mpl.rcParams['font.family'] = 'AR PL UKai CN '
# 字体大小
mpl.rcParams['font.size'] = 12
# 正常显示负号
cols = ['顾客ID', '购买日期', '购买产品', '消费金额']
# 顾客ID 购买日期 购买产品 消费金额
df_data = pd.read_table("客户数据消费.txt", names=cols, sep='\s+')

# 转换购买日期字段的数据类型为时间类型，format ='%Y%m%d'表示年月日。
df_data['购买日期'] = pd.to_datetime(df_data.购买日期, format="%Y%m%d")
# 在df_data里增加一列：月份，并将其类型设置为日期类型
df_data['月份'] = df_data.购买日期.values.astype('datetime64[M]')
# 去掉时分秒
df_data['月份'] = df_data['月份'].dt.date
# 查看当前df_data的数据内容
# df_data
# 查看当前df_data的数据描述信息
# df_data.describe()
# 按月分析数据趋势
# 按月分组
gp_month = df_data.groupby('月份')
# 使用sum函数计算每月消费总金额
month_spend = gp_month.消费金额.sum()
# 使用sum函数计算每月产品总数
month_total = gp_month.购买产品.sum()
# 使用count函数计算每月用户总数
month_persons = gp_month.顾客ID.count()
# 使用plot函数绘制month_spend的柱状图，month_total的折线图，month_persons的饼图数据
# 每月消费总金额
# month_spend.plot(kind="bar",color="red")
# 每月购买产品总数
# month_total.plot(color="blue")
# 每月用户总数
month_persons.plot(kind="pie", autopct='%1.0f%%', fontsize=10)
plt.show()
# 每月消费人数，使用groupby函数根据月份字段进行分组，nunique表示去重
df_data.groupby('月份').顾客ID.nunique().plot()
plt.show()
# 单个客户消费数据分析
# 使用groupby根据顾客ID进行分组
gp_cusID = df_data.groupby('顾客ID')
# 查看gp_cusID的数据求和后的描述信息
# print(gp_cusID.sum().describe())
# 使用groupby根据顾客ID进行分组
gp_cusID = df_data.groupby('顾客ID')
# 使用sum函数求和之后，使用query函数查询消费金额<1000的数据，并使用scatter函数将所得数据的消费金额字段作为x轴，购买产品作为y轴。
# gp_cusID.sum().query("消费金额<1000").plot.scatter(x = '消费金额',y = '购买产品')
# 使用sum函数根据顾客ID求和之后根据query函数查询购买产品<30的数据之中购买产品的数据绘制直方图，bins = 40表示分成40组数据。
gp_cusID.sum().query("购买产品<30").购买产品.plot.hist(bins=40)
# 显示直方图
plt.show()
# 用户的累计消费金额占比
# 根据顾客ID求和之后，按照消费金额字段进行排序，cumsum方法是滚动求和
cum1 = gp_cusID.sum().sort_values("消费金额").apply(lambda x: x.cumsum() / x.sum())
# 使用reset_index函数对排序之后的数据索引进行重置
cum1.reset_index().消费金额.plot()
plt.show()
#  用户消费行为分析
# 根据顾客ID提取月份的min最小值：表示用户第一次消费的时间集中的月份和次数
print(gp_cusID.月份.min().value_counts())
# 根据顾客ID提取月份的max最大值：表示用户最后一次消费的时间集中的月份和次数
print(gp_cusID.月份.max().value_counts())
gp_cusID.月份.min().value_counts().plot()
gp_cusID.月份.max().value_counts().plot()
# 使用聚合函数agg，根据gp_cusID的购买日期字段求出用户第一次和最后一次购买时间。
new = gp_cusID.购买日期.agg(['min', 'max'])
# 如果new['min']==new['max']则表示：该用户第一次和最后一次购买是同一时间，就可能是流失的客户数。
print((new['min'] == new['max']).value_counts())
# exit()
# 使用pivot_table函数实现df的数据透视表功能,index表示索引,values表示字段,aggfunc表示聚合函数(max:求最大值,sum:求和)
df_rfm = df_data.pivot_table(index='顾客ID',
                             values=['购买产品', '消费金额', '购买日期'],
                             aggfunc={'购买日期': 'max', '消费金额': 'sum', '购买产品': 'sum'})
# 查看rfm的数据透视表
# df_rfm
# 根据购买日期与最后一次购买日期相减,再除以按天D计算的时间格式,得到用户最近一次交易时间间隔rfm["R"].
df_rfm["R"] = -(df_rfm.购买日期 - df_rfm.购买日期.max()) / np.timedelta64(1, 'D')
# 使用rename函数将消费金额重命名为M,购买产品重命名为F
df_rfm.rename(columns={'消费金额': 'M', '购买产品': 'F'}, inplace=True)
# print(df_rfm)
# exit()
# 使用apply(lambda x: x - x.mean())求出每个用户ID的R,F,M各自与平均值相减后的正负值.正表示高于平均值,负表示低于平均值.
# print(df_rfm[["R", 'F', "M"]].apply(lambda x: x - x.mean()))


# 自定义函数aggfc,用于接收rfm[["R", 'F', "M"]].apply(lambda x: x - x.mean())的返回值,.
def aggfc(k):
    # 根据"R", 'F', "M"的正负值对用户进行分类:正数用1表示,负数用0表示.
    level = k.apply(lambda x: '1' if x > 0 else '0')
    leable = level.R + level.M + level.F
    # 根据正负数编码,将用户分为8类型
    d = {
        '111': '1类客户',
        '011': '2类客户',
        '101': '3类客户',
        '001': '4类客户',
        '110': '5类客户',
        '010': '6类客户',
        '100': '7类客户',
        '000': '8类客户'
    }
    result = d[leable]
    return result


#  使用自定义函数aggfc对用户进行分类,并赋值给新的字段label.
df_rfm['label'] = df_rfm[["R", 'F', "M"]].apply(lambda x: x - x.mean()).apply(aggfc, axis=1)
# 根据label字段进行分组,并求和.
# print(df_rfm.groupby('label').sum())
# 根据label字段进行分组,并统计个数.
# print(df_rfm.groupby('label').count())
# 根据lable标签查找2类客户数据,并用g绿色标注
df_rfm.loc[df_rfm.label == '2类客户', 'color'] = 'g'
# 根据lable标签查找非2类客户数据,并用r红色标注
df_rfm.loc[~(df_rfm.label == '2类客户'), 'color'] = 'r'
# 使用scatter将F和R作为参数,颜色使用前面的g和r.
df_rfm.plot.scatter("F", 'R', c=df_rfm.color)
plt.show()
# exit()
# 设置自定义时间字段用于索引
cols = ['2020-01-01', '2020-02-01', '2020-03-01', '2020-04-01',
        '2020-05-01', '2020-06-01', '2020-07-01', '2020-08-01',
        '2020-09-01', '2020-10-01', '2020-11-01', '2020-12-01',
        '2021-01-01', '2021-02-01', '2021-03-01', '2021-04-01',
        '2021-05-01', '2021-06-01']


# 自定义函数active_status用于区分活跃,不活跃,回流和新用户的四类用户
# 这里的区分四类用户的标准根据前面的
def active_status(data):
    status = []
    # 因为上面的col自定义了18个字段,所以每行有18个数据,因此这里要循环18次.
    for i in range(18):

        # 若本月没有消费
        if data[i] == 0:
            if len(status) > 0:
                if status[i - 1] == 'unreg':  # unreg未注册用户
                    status.append('unreg')
                else:
                    status.append('unactive')  # 不活跃用户
            else:
                status.append('unreg')

        # 若本月消费
        else:
            if len(status) == 0:
                status.append('new')
            else:
                if status[i - 1] == 'unactive':
                    status.append('return')  # 回流用户
                elif status[i - 1] == 'unreg':
                    status.append('new')  # 新用户
                else:
                    status.append('active')  # 活跃用户
    return pd.Series(status, index=cols)


# 使用pivot_table透视表功能,将df数据设置为:index索引:顾客ID,values列:购买日期,
# columns列细分通用名:月份,aggfunc聚合函数为count,并使用fillna填充na为0.
pivot_count = df_data.pivot_table(index='顾客ID', columns='月份', values='购买日期', aggfunc='count').fillna(0)
# 使用applymap(lambda x:1 if x>0 else 0)根据统计结果进行分类
df_spend = pivot_count.applymap(lambda x: 1 if x > 0 else 0)
# 使用apply( active_status,axis = 1)按行进行传递给自定义函数active_status
pivot_statu = df_spend.apply(active_status, axis=1)
# 输出前5行
# pivot_statu.head()
# 使用replace('unreg',np.NAN)将np.NAN替换为unreg,并统计个数.
# print(pivot_statu.replace('unreg', np.NAN).apply(lambda x: pd.value_counts(x)))
# 统计每月活跃,新用户,回流用户和不活跃用户的占比
pivot_statu = df_spend.apply(active_status, axis=1)
new_point = pivot_statu.replace('unreg', np.NAN).apply(lambda x: pd.value_counts(x))
# 按行axis = 1统计每月活跃,新用户,回流用户和不活跃用户的占比x:x/x.sum(),使用fillna填充缺失值为0.
# print(new_point.fillna(0).T.apply(lambda x: x / x.sum(), axis=1))
# 使用pivot_table函数透视表，index索引为用户ID，values列为订购数量，
# columns列细分通用名为月份，aggfunc聚合函数为mean，fillna填充缺失值为0
pivot_amount = df_data.pivot_table(index='顾客ID', columns='月份', values='消费金额', aggfunc='mean').fillna(0)
# 根据订购金额的多少判断为1或0，0代表当月消费过次月没有消费过，1代表当月消费过次月依然消费
pivot_spend = pivot_amount.applymap(lambda x: 1 if x > 0 else 0)
# 根据月份字段进行排序，并转换类型为字符串，再去重。
col_month = df_data.月份.sort_values().astype('str').unique()
# 给pivoted_amount的列细分通用名修改为：columns_month
pivot_amount.columns = col_month


# 自定义函数purchase_return用于统计回流客户
def purchase_return(data):
    status = []
    for i in range(17):
        if data[i] == 1:
            if data[i + 1] == 1:
                status.append(1)
            if data[i + 1] == 0:
                status.append(0)
        else:
            status.append(np.NaN)
    status.append(np.NaN)
    return pd.Series(status, index=cols)


# 根据前面统计的订购金额情况（0或1），输入到函数purchase_return中，得出回流用户数据
pivot_spend_return = pivot_spend.apply(purchase_return, axis=1)
# 老客的回购率计算
(pivot_spend_return.sum() / pivot_spend_return.count()).plot()
plt.xticks(rotation=45)  # 横坐标的数据旋转45°
plt.show()
