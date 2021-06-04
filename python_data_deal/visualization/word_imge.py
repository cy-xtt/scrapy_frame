import pandas as pd
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
import jieba
import wordcloud
import re
from pyecharts import options as opts
from pyecharts.charts import Geo,Map,Bar,Line
from pyecharts.globals import ChartType

matplotlib.rcParams['font.sans-serif'] = ['SimHei']
matplotlib.rcParams['axes.unicode_minus'] = False

data = pd.read_csv(r'E:\Program Files\JetBrains\pycharm zy\python_qm\python_data_deal\重庆九区_a.csv',encoding='gbk')
df = data[['核心卖点','小区介绍','交通出行','户型介绍']][0:-5]
print(df)
def imge_x(x):
    str_comment = df[x].apply(str)
    str_comment = ''.join(str_comment)
    cut_list = re.compile('\s|\d|/|').sub('', str_comment)
    cut_list = jieba.lcut_for_search(cut_list)

    stop_list = []
    with open(r'E:\大三\综合实训\stopwords-master\cn_stopwords.txt','r',encoding='utf-8') as f:
        stop_date = f.read()
        stop_list += stop_date.split('\n')
    with open(r'E:\大三\综合实训\stopwords-master\hit_stopwords.txt', 'r', encoding='UTF-8') as f:
        stopword_str = f.read()
        stop_list += stopword_str.split('\n')
    data_1 = [i for i in cut_list if i not in stop_list]
    sort_data = pd.Series(data_1).value_counts()
    print(sort_data)
    wc = wordcloud.WordCloud(background_color='white',font_path=r'C:\Windows\Fonts\simkai.ttf',mask=plt.imread('./房子.jpg'))
    print(type(sort_data))
    wc.fit_words(sort_data[:200])
    plt.imshow(wc)
    plt.title('{}词云图'.format(x))
    plt.show()
list_1 = ['核心卖点','小区介绍','交通出行','户型介绍']
for i in list_1:
    imge_x(i)