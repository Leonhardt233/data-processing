# 导入pandas
import pandas as pd

# 使用object类型读取数据
sale_data = pd.read_excel("超市水果销售数据.xlsx", dtype="object")
# 使用info函数查看sale_data数据类型
sale_data.info()
# 转换为DataFrame 格式
df_result = pd.DataFrame(sale_data)
# 查看源数据前面10行数据
df_result.head(10)

# 查看每一列数据统计数目
df_result.count()
# 使用 rename 函数，把"出售时间" 改为 "销售日期"
df_result.rename(columns={"出售时间": "销售日期"}, inplace=True)

# 删除缺失值之前

# 使用dropna函数删除缺失值
df_result = df_result.dropna()

# 查看处理缺失值后的结果
df_result.isnull()
# 将字符串转为浮点型数据
df_result["购买斤数"] = df_result["购买斤数"].astype("f8")
df_result["消费总额"] = df_result["消费总额"].astype("f8")
df_result["实收金额"] = df_result["实收金额"].astype("f8")


# 定义函数将星期去除
def splitsaleweek(timeColser):
    datelist = []
    for t in timeColser:
        datelist.append(t.split(" ")[0])  # [0]表示选取的分片，这里表示切割完后选取第一个分片
    timeser = pd.Series(datelist)  # 将列表转行为一维数据Series类型
    return timeser


# 获取"销售日期"这一列数据
t = df_result.loc[:, "销售日期"]
# 调用函数去除星期，获取日期
timeser = splitsaleweek(t)
# 修改"销售日期"这一列日期
df_result.loc[:, "销售日期"] = timeser
df_result.head(10)
# 字符串转日期
# errors='coerce'如果原始数据不符合日期的格式，转换后的值为NaT
df_result.loc[:, "销售日期"] = pd.to_datetime(df_result.loc[:, "销售日期"], errors='coerce')

# 转换日期过程中不符合日期格式的数值会被转换为空值None，
# 这里删除为空的行
df_result = df_result.dropna()

# 按销售日期进行升序排序
df_result = df_result.sort_values(by='销售日期', ascending=True)
df_result.head()
# 重置索引（index）
df_result = df_result.reset_index(drop=True)
df_result.head()
# 查看描述统计信息
df_result.describe()
# 将"购买斤数"这一列中小于0的数排除掉
pop = df_result.loc[:, "购买斤数"] > 0
df_result = df_result.loc[pop, :]
# 排除异常值后再次查看描述统计信息
df_result.describe()
# 删除重复数据
df_kpi1 = df_result.drop_duplicates(subset=['销售日期', '客户ID'])
# 总消费次数
total = df_kpi1.shape[0]
print('总消费次数：', total)
# 按销售时间升序排序
df_kpi1 = df_kpi1.sort_values(by='销售日期', ascending=True)
# 重命名行名（index）
df_kpi1 = df_kpi1.reset_index(drop=True)

# 获取时间范围
# 最小时间值
startDate = df_kpi1.loc[0, '销售日期']
# 最大时间值
endDate = df_kpi1.loc[total - 1, '销售日期']
# 计算天数
days_1 = (endDate - startDate).days
# 月份数：运算符"//"表示取整除，返回商的整数部分
months_1 = days_1 // 30
print('月份数：', months_1)
# 计算月均消费次数
kpi1_1 = total // months_1
print('业务指标1：月均消费次数=', kpi1_1)
# 总消费金额
Totalconsumption = df_result.loc[:, '实收金额'].sum()

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
df_result1 = df_result
# 重命名行（index）为销售时间所在列的值
df_result1.index = df_result1['销售日期']
df_result1.head(10)
import matplotlib.pyplot as plt

# 使用柱状图呈现实收金额和日期的关系
plt.plot(df_result1['实收金额'], color='y')
plt.title('按天消费金额图')
plt.xlabel('时间')
plt.ylabel('实收金额')
# 保存图片
plt.savefig('./day.png')
# 显示图片
plt.show()
# 将销售时间聚合按月分组
month_group = df_result1.groupby(df_result1.index.month)
# 应用函数，计算每个月的消费总额
df_month = month_group.sum()

# 描绘按月消费金额图
plt.bar(df_month.index, df_month['实收金额'], color='r')
plt.title('按月消费金额图')
plt.xlabel('月份')
plt.ylabel('实收金额')
# 保存图片
plt.savefig('./month.png')
# 显示图片
plt.show()
# 聚合统计各种水果的销售数量
fruits = df_result1[['水果名', '购买斤数']]
fruits_1 = fruits.groupby('水果名')[['购买斤数']]
re_fruits = fruits_1.sum()
# 对水果购买数量按降序排序
re_fruits = re_fruits.sort_values(by='购买斤数', ascending=False)
re_fruits.head()
# 截取销售数量最多的十种水果
top_fruits = re_fruits.iloc[:10, :]

# 用饼图展示销售数量前十的水果
top10_fruits = top_fruits['购买斤数']
top10_fruits.plot(kind='pie', autopct='%1.1f%%', title='水果销售前十情况')
# 保存图片
plt.savefig('./fruits.png')
# 显示图片
plt.show()
