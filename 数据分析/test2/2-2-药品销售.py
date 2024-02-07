# 导入pandas
import pandas as pd

# 使用object类型读取数据
data = pd.read_excel("药品销售数据.xlsx", dtype="object")
# 使用info函数查看sale_data数据类型
data.info()
# 转换为DataFrame 格式
dataDF = pd.DataFrame(data)
# 查看源数据前面10行数据
dataDF.head(10)

# 查看每一列数据统计数目
dataDF.count()
dataDF.rename(columns={"购药时间": "销售时间"}, inplace=True)
# 用dropna函数删除缺失值
dataDF = dataDF.dropna()
# 查看处理缺失值后的结果
dataDF.isnull()
# 将字符串转为浮点型数据
dataDF["销售数量"] = dataDF["销售数量"].astype("f8")
dataDF["应收金额"] = dataDF["应收金额"].astype("f8")
dataDF["实收金额"] = dataDF["实收金额"].astype("f8")

# 定义函数将星期去除
def splitsaleweek(timeColser):
    datelist = []
    for t in timeColser:
        datelist.append(t.split(" ")[0])  # [0]表示选取的分片，这里表示切割完后选取第一个分片
    timeser = pd.Series(datelist)  # 将列表转行为一维数据Series类型
    return timeser


# 获取"销售日期"这一列数据
t = dataDF.loc[:, "销售时间"]
# 调用函数去除星期，获取日期
timeser = splitsaleweek(t)
# 修改"销售日期"这一列日期
dataDF.loc[:, "销售时间"] = timeser
dataDF.head(10)
# 字符串转日期
# errors='coerce'如果原始数据不符合日期的格式，转换后的值为NaT
dataDF.loc[:, "销售时间"] = pd.to_datetime(dataDF.loc[:, "销售时间"], errors='coerce')

# 转换日期过程中不符合日期格式的数值会被转换为空值None，
# 这里删除为空的行
dataDF = dataDF.dropna()

# 按销售日期进行升序排序
dataDF = dataDF.sort_values(by='销售时间', ascending=True)
dataDF.head()
# 重置索引（index）
dataDF = dataDF.reset_index(drop=True)
dataDF.head()
# 查看描述统计信息
dataDF.describe()
# 将"销售数量"这一列中小于0的数排除掉
pop = dataDF.loc[:, "销售数量"] > 0
dataDF = dataDF.loc[pop, :]
# 排除异常值后再次查看描述统计信息
dataDF.describe()
# 删除重复数据
kpi1_DF = dataDF.drop_duplicates(subset=['销售时间', '社保卡号'])
# 总消费次数
total = kpi1_DF.shape[0]
print('总消费次数：', total)
# 按销售时间升序排序
kpi1_DF = kpi1_DF.sort_values(by='销售时间', ascending=True)
# 重命名行名（index）
kpi1_DF = kpi1_DF.reset_index(drop=True)

# 获取时间范围
# 最小时间值
startDate = kpi1_DF.loc[0, '销售时间']
# 最大时间值
endDate = kpi1_DF.loc[total - 1, '销售时间']
# 计算天数
days_1 = (endDate - startDate).days
# 月份数：运算符"//"表示取整除，返回商的整数部分
months_1 = days_1 // 30
print('月份数：', months_1)
# 计算月均消费次数
kpi1_1 = total // months_1
print('业务指标1：月均消费次数=', kpi1_1)
# 总消费金额
Totalconsumption = dataDF.loc[:, '实收金额'].sum()

# 月均消费金额
monthconsumption = Totalconsumption / months_1
print('业务指标2：月均消费金额=', monthconsumption)
# 客户人均消费金额 = 总消费金额 / 总消费次数
pcc = Totalconsumption / total
print('业务指标3：客户人均消费金额=', pcc)
import matplotlib as mpl

# 汉字字体,优先使用楷体，如果找不到楷体，则使用黑体
mpl.rcParams['font.sans-serif'] = ['KaiTi', 'SimHei', 'FangSong']
# 字体大小
mpl.rcParams['font.size'] = 12
# 正常显示负号
mpl.rcParams['axes.unicode_minus'] = False
# 在操作之前先复制一份数据，防止影响清洗后的数据
df_result1 = dataDF
# 重命名行（index）为销售时间所在列的值
df_result1.index = df_result1['销售时间']
df_result1.head(10)
import matplotlib.pyplot as plt

# 使用柱状图呈现实收金额和日期的关系
plt.plot(dataDF['实收金额'])
plt.title('按天消费金额图')
plt.xlabel('时间')
plt.ylabel('实收金额')
plt.show()
# 将销售时间聚合按月分组
month_group = df_result1.groupby(df_result1.index.month)
# 应用函数，计算每个月的消费总额
df_month = month_group.sum()

# 描绘按月消费金额图
plt.plot(df_month['实收金额'])
plt.title('按月消费金额图')
plt.xlabel('月份')
plt.ylabel('实收金额')
# 显示图片
plt.show()
# 聚合统计各种药品的销售数量
medicine = df_result1[['商品名称', '销售数量']]
bk = medicine.groupby('商品名称')[['销售数量']]
re_medicine = bk.sum()
# 对水果购买数量按降序排序
re_medicine = re_medicine.sort_values(by='销售数量', ascending=False)
# re_medicine.head()
# 截取销售数量最多的十种水果
top_medicine = re_medicine.iloc[:10, :]

# 用饼图展示销售数量前十的水果
top_medicine.plot(kind='bar')
plt.title("药品销售前十情况")
plt.xlabel('药品种类')
plt.ylabel('销售数量')
plt.legend(loc=0)

# 显示图片
plt.show()
