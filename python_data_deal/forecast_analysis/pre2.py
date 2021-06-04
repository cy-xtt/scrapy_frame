import pandas as pd
import numpy as np
from sklearn.tree import DecisionTreeRegressor #决策树回归
from sklearn.model_selection import train_test_split #划分测试集和训练集
from sklearn.metrics import r2_score #评价方法
from sklearn.svm import LinearSVR #向量机
from sklearn.decomposition import PCA
import matplotlib.pyplot as plt
from sklearn.externals import joblib
from sklearn.model_selection import KFold
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import make_scorer,accuracy_score
from sklearn.model_selection import GridSearchCV
from sklearn.naive_bayes import GaussianNB #贝叶斯
from sklearn.ensemble import RandomForestRegressor #随机森林
from sklearn.neighbors import RadiusNeighborsRegressor

from sklearn.svm import SVR
plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']


data = pd.read_csv('..//重庆九区_a.csv',encoding='utf-8')
data.dropna(subset=['套内面积'], inplace=True)
# list_5 = []
# for i in data['楼层']:
#     m = i.strip()
#     if len(m)<5:
#         j = ''
#         list_5.append(j)
#     else:
#         j = m[0:3]
#         list_5.append(j)
# data['楼层'] = list_5
# data = data[data['楼层'] != '']

df = data[['地址','价格','每平米价格','所属地区','套内面积',
           '挂牌时间','房子总面积','朝向','装修程度','楼层',
           '建筑年代','楼型','室','厅','厨','卫','多少人关注']]

df['挂牌时间'] = pd.to_datetime(df['挂牌时间'])
df.set_index('挂牌时间',inplace=True)
#df = df['2020']

d = pd.get_dummies(df['楼层'])  #one-hot编码
m = pd.get_dummies(df['朝向'])
c = pd.get_dummies(df['装修程度'])
a = pd.get_dummies(df['所属地区'])
e = pd.get_dummies(df['建筑年代'])
f = pd.get_dummies(df['楼型'])
df = pd.concat([df,d,m,c,a,e,f],axis=1)
df.drop(['楼层','朝向','装修程度','所属地区','建筑年代','楼型'],axis=1,inplace=True)
#计算相关系数
corrDf = df.corr()

print(corrDf['价格'].sort_values(ascending =False))
#选取相关系数较高的前11项
df_1 = df[['房子总面积','每平米价格','卫','室','套内面积','厅','江北','渝北','渝中',' 毛坯 ','价格',' 板楼']]
x = df_1[['房子总面积','套内面积','卫','室','厅','江北','渝北','渝中',' 毛坯 ']].values.tolist()
y = df_1['价格'].values.tolist()
train_x,test_x,train_y,test_y = train_test_split(x,y,test_size=0.2,random_state=0)
# model = GaussianNB()
# model.fit(train_x,train_y)
# pre_y = model.predict(test_x)
# print(pre_y)
from sklearn.neural_network import MLPRegressor
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.linear_model.stochastic_gradient import SGDRegressor
from sklearn.ensemble import AdaBoostRegressor
from sklearn.ensemble import GradientBoostingRegressor
#gp = GaussianProcessRegressor()
from sklearn.neighbors import KNeighborsRegressor
# gp = SVR(C=500)
# gp.fit(train_x,train_y)
#gp = SGDRegressor(max_iter=10)
#gp = KNeighborsRegressor(n_neighbors=20,weights='distance',p=1)
#gp = RadiusNeighborsRegressor(radius=1.0)
#gp = MLPRegressor(hidden_layer_sizes=(200,50,1),alpha=0.5,random_state=1, max_iter=500,activation='relu',learning_rate="adaptive")

gp = GradientBoostingRegressor(random_state=100,n_estimators=100,max_depth=3)
#gp = AdaBoostRegressor(random_state=100, n_estimators=1000,loss='linear',learning_rate=0.5)
gp.fit(train_x,train_y)
joblib.dump(gp,'./keep_model/model.pkl')
pre_y = gp.predict(test_x)
print(r2_score(test_y,pre_y))
plt.figure(figsize=(10,9),dpi=100)
plt.plot(test_y,label='实际值')
plt.plot(pre_y,label='预测值')
plt.legend()
plt.title('实际值与预测值对比')
plt.show()