import pandas as pd
import numpy as np
import imge


data = pd.read_csv('../重庆九区_a.csv')
data.dropna(subset=['套内面积'], inplace=True)
data_1 = data.drop_duplicates(subset='所属地区', keep='first')
df = data[['所属地区','挂牌时间','多少人关注','房屋类型','楼型']]
df['挂牌时间'] = pd.to_datetime(df['挂牌时间'])
df.set_index('挂牌时间',inplace=True)
df_1 = df['2020']
g1 = df_1.sort_values(by='多少人关注', ascending=False)
g1_1 = g1['所属地区'][:500]
x_1 = g1_1.value_counts()
title_1 = '2020年以来受欢迎的二手房在各地区的占比'
print(x_1)
imge.pie_img(x_1,x_1.index,title_1)

g1_2 = g1['房屋类型'][:50]
x_2 = g1_2.value_counts()

title_2 = '2020年以来受欢迎的房型'

#imge.pie_img(x_2,x_2.index,title_2)


#g1_3_1 = g1[g1['楼型'] != ' 暂无数据']
g1_3 = g1['楼型'][:500]
x_3 = g1_3.value_counts()
title_3 = '受欢迎楼的类型'
#imge.pie_img(x_3,x_3.index,title_3)


def esf_orientation(data):
    data['总金额'] = data['房子总面积']*data['每平米价格']
    group = data.groupby(by='朝向', as_index=False).agg({'房子总面积':np.sum,'总金额':np.sum,'所属地区':np.size})
    group['均价'] = np.round(group['总金额']/group['房子总面积'],2)
    #按数量进行排序
    group.sort_values(by=['所属地区'],ascending=False,inplace=True)
    print(group)
    #取前面5重户型,来绘制条形图
    temp = group.iloc[:5,:]
    x = temp['朝向']
    y = temp['均价']
    title = '热门户型朝向前五均价'
    imge.bar_img(x,y,title)

esf_orientation(data)
