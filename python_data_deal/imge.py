import pandas as pd
from matplotlib import pyplot as plt

plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']


def pie_img(x,label,title): #x是一个向量,label标签向量,长度要求一致
    if len(x) != len(label):
        print('数据长度不对')
    else:
        plt.figure(figsize=(10,8),dpi=100)
        plt.pie(x,labels=label,autopct='%0.02f%%')
        plt.legend()
        plt.title(title)
        plt.show()

def line_img(x,y,title): #x表示横坐标从小到大排列,y表示纵坐标,长度一致
    if len(x) != len(y):
        print('长度不一致')
    else:
        data = pd.DataFrame({'x': x, 'y': y})
        data.sort_values(by='x',inplace=True)
        plt.plot(data['x'].values.tolist(),data['y'].values.tolist())
        plt.legend()
        plt.title(title)
        plt.show()

def bar_img(x,y,title):
    if len(x) != len(y):
        print('长度不一致')
    else:
        plt.figure(figsize=(10,8),dpi=100)
        plt.bar(x,y)
        for x,y in zip(x,y):
            plt.text(x,y+0.1,y)
        plt.title(title)
        plt.show()

