import pandas as pd
import numpy as np
import imge




#各区域二手房每平方米均价分析
def esf_average(data):
    group1 = data.groupby(by='所属地区',as_index=False)['每平米价格'].mean()
    x = group1['所属地区'].values.tolist()
    y = np.round(group1['每平米价格'].values.tolist(),2)
    title_x = '各区域二手房每平米均价分析'
    imge.bar_img(x,y,title=title_x)


#各个地区装修程度
def esf_decorate(data):
    data_1 = data.drop_duplicates(subset='所属地区',keep='first')
    group = data.groupby(by='装修程度',as_index=False)['所属地区'].count()
    x = group['装修程度'].values.tolist()
    y = group['所属地区'].values.tolist()
    title = '二手房装修情况'
    imge.bar_img(x,y,title=title)




if __name__=='__main__':
    data = pd.read_csv('重庆九区_a.csv')
    data.dropna(subset=['套内面积'], inplace=True)
    #esf_average(data)
    esf_decorate(data)

