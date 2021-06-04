import pymysql
import pandas as pd
import datetime



conn = pymysql.connect(host='localhost',user='root',password='123456',db='python_qm_scrapy',charset='gbk')
cursor = conn.cursor()
cursor.execute("USE python_qm_scrapy")
sql = 'select * from python_qm_scrapy.scrapy_2_house'
cursor.execute(sql)
data = list(cursor.fetchall())
data = pd.DataFrame(data)
data.columns = ['名称','详情页链接','多少人关注以及多久前发布的','地址','房屋信息','价格','每平米价格',
               '所属地区','房屋类型','套内面积','挂牌时间','上一次交易时间','核心卖点','小区介绍',
               '交通出行','户型介绍']
data.drop('详情页链接',axis=1,inplace=True)
data1 = data['多少人关注以及多久前发布的'].str.split('/',expand=True)
data1.columns = ['多少人关注','多久前发布']
data = pd.concat([data,data1],axis=1)
data.drop('多少人关注以及多久前发布的',axis=1,inplace=True)
data2 = data['房屋信息'].str.split('|',expand=True)
data2.columns = ['几室几厅_1','房子总面积','朝向','装修程度','楼层','建筑年代','楼型','空']
data2.drop(columns=['空','几室几厅_1'],axis=1,inplace=True)
data = pd.concat([data,data2],axis=1)
data.drop('房屋信息',axis=1,inplace=True)
print(data.columns)

data['多少人关注'] = data['多少人关注'].apply(lambda x:float(x[0:-4]))
data['每平米价格'] = data['每平米价格'].apply(lambda x:float(x[2:-4]))
data['房子总面积'] = data['房子总面积'].apply(lambda x:float(x[0:-3]))
data['价格'] = data['价格'].astype(float)

#处理套内面积 转换为flaot
list_measure = []
for j in data['套内面积']:
    if j != '暂无数据':
        k = j[0:-1]
        list_measure.append(k.strip())
    else:
        list_measure.append(j)
data['套内面积'] = list_measure
data = data[(data['套内面积'] != '东') & (data['套内面积'] != '南') & (data['套内面积'] != '南 北') & (data['套内面积'] != '西南') & (data['套内面积'] != '东南')]
data = data[(data['套内面积'] != '东 南') & (data['套内面积'] != '东 东南') & (data['套内面积'] != '西') & (data['套内面积'] != '北') & (data['套内面积'] != '东 东')]



data[['室','厅','厨','卫']] = data['房屋类型'].str.extract('(\d)室(\d)厅(\d)厨(\d)卫')
#data.drop('房屋类型',axis=1,inplace=True)
data['室'] = data['室'].astype(float)
data['厅'] = data['厅'].astype(float)
data['厨'] = data['厨'].astype(float)
data['卫'] = data['卫'].astype(float)
data['挂牌时间'] = pd.to_datetime(data['挂牌时间'])

#处理挂牌时间的异常值
list_time = []
for i in data['上一次交易时间']:
    if i != '暂无数据' and float(i[0:4]) > 2020:
        m = 1
        list_time.append(m)
    else:
        n = 0
        list_time.append(n)
data['上一次交易时间的异常数据'] = list_time
#data['上一次交易时间'] = pd.to_datetime(data['上一次交易时间'])
print(len(data['上一次交易时间的异常数据']))
data = data[data['上一次交易时间的异常数据'] == 0]
print(len(data['上一次交易时间的异常数据']))
data.drop('上一次交易时间的异常数据',axis=1,inplace=True)

list_2 =[]
for i,j in zip(data['建筑年代'],data['楼型']):
    if j == None:
        list_2.append(i)
    else:
        list_2.append(j)
data['楼型'] = list_2
print(data.isnull().sum())

list_3 = []
for i in data['建筑年代']:
    if len(i) < 4:
        m = '暂无数据'
        list_3.append(m)
    elif i == ' 板塔结合':
        j = '暂无数据'
        list_3.append(j)
    elif i == ' 板塔结合 ' or i == ' 板楼 ' or i == ' 塔楼 ':
        j = '暂无数据'
        list_3.append(j)
    else:
        list_3.append(i)
data['建筑年代'] = list_3




def change_zw(x):
    #df = pd.DataFrame()
    df = data[['地址',x, '房屋类型']]
    df_no = df[df[x] != '暂无数据']
    df_no_1 = df_no.drop_duplicates(subset=['地址', '房屋类型'], keep='first')
    for i, j, l, o in zip(data['地址'],data[x],data['房屋类型'],range(len(data))):
        for n, m, k in zip(df_no_1['地址'],df_no_1[x],df_no_1['房屋类型']):
            if j == '暂无数据' and i==n and l==k:
                data[x].replace(data[x][o],m,inplace=True)
                break


list_4 = ['建筑年代','楼型','套内面积']
for i in list_4:
    change_zw(i)
data.dropna(axis=0,how='any',inplace=True)
# print(data.isnull().sum())
print(data.dtypes)
#data.to_csv('重庆九区_a.csv',index=False)
