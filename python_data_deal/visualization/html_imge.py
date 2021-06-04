import pandas as pd
import numpy as np
from pyecharts import options as opts
from pyecharts.charts import Bar


data = pd.read_csv('../重庆九区_a.csv')
data.dropna(subset=['套内面积'], inplace=True)
data_1 = data.drop_duplicates(subset='所属地区', keep='first')
list_r = [' 其他 ', ' 毛坯 ', ' 简装 ', ' 精装 ']
list_roughcast = [] #毛坯
list_paperback = [] #简装
list_hardcover = [] #精装
list_other = [] #其他
for i in data_1['所属地区']:
    df = data[data['所属地区'] == i]
    df_1 = df[df['装修程度'] == ' 毛坯 ']
    df_2 = df[df['装修程度'] == ' 简装 ']
    df_3 = df[df['装修程度'] == ' 精装 ']
    df_4 = df[df['装修程度'] == ' 其他 ']
    list_roughcast.append(len(df_1))
    list_paperback.append(len(df_2))
    list_hardcover.append(len(df_3))
    list_other.append(len(df_4))
list_add = []
for i in data_1['所属地区']:
    list_add.append(i)
c = (
    Bar()
    .add_xaxis(list_add)
    .add_yaxis('毛坯',list_roughcast)
    .add_yaxis('简装',list_paperback)
    .add_yaxis('精装',list_hardcover)
    .add_yaxis('其他',list_other)
    .set_global_opts(
        title_opts=opts.TitleOpts(title='各地区二手房装修程度数量表'),
        yaxis_opts=opts.AxisOpts(name='二手房数量'),
        xaxis_opts=opts.AxisOpts(name='城市')

    )
)
c.render('各地区二手房装修程度数量表.html')