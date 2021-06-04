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
from sklearn.preprocessing import StandardScaler #数据的标准化


plt.rcParams['font.family'] = ['sans-serif']
plt.rcParams['font.sans-serif'] = ['SimHei']


data = pd.read_csv('../重庆九区_a.csv',encoding='gbk')
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
#df.set_index('挂牌时间',inplace=True)
#df = df['2020']

d = pd.get_dummies(df['楼层'])  #one-hot编码
m = pd.get_dummies(df['朝向'])
c = pd.get_dummies(df['装修程度'])
a = pd.get_dummies(df['所属地区'])
e = pd.get_dummies(df['建筑年代'])
f = pd.get_dummies(df['楼型'])
df = pd.concat([df,d,m,c,a,e,f],axis=1)
df.drop(['楼层','朝向','装修程度','所属地区','建筑年代','楼型'],axis=1,inplace=True)
df_1 = df[0:-5]
df_2 = df[-5:]

#计算相关系数
#corrDf = df.corr()
#print(corrDf['价格'].sort_values(ascending =False))
#选取相关系数较高的前11项
#df_1 = df[['房子总面积','每平米价格','卫','室','套内面积','厅','江北','渝北','渝中',' 毛坯 ','价格',' 板楼']]
x = df_1[['房子总面积','套内面积','渝北','江北','沙坪坝','南岸','九龙坡','渝中','巴南','大渡口','北碚','室','厅','厨','卫',' 毛坯 ',' 简装 ',' 精装 ',' 塔楼',' 板楼',' 板塔结合']].values.tolist()
y = df_1['价格'].values.tolist()
train_x,test_x,train_y,test_y = train_test_split(x,y,test_size=0.2,random_state=100)
std = StandardScaler()
model_std = std.fit(train_x)
train_x_std = model_std.transform(train_x)
test_x_std = model_std.transform(test_x)


#决策树模型

def performance_metric(y_true, y_predict):
    from sklearn.metrics import r2_score
    score = r2_score(y_true,y_predict)
    return score


def fit_model(x, y):
    cross_validator = KFold(n_splits=3,shuffle=True, random_state=0) #交叉验证
    #regressor = DecisionTreeRegressor(random_state=0) #决策树回归函数
    from sklearn.tree import ExtraTreeRegressor  #极端二叉树
    from sklearn.neighbors import KNeighborsRegressor
    from sklearn.ensemble import GradientBoostingRegressor
    #regressor = KNeighborsRegressor()
    #regressor = ExtraTreeRegressor(random_state=0)
    regressor = GradientBoostingRegressor(loss='ls',random_state=100,max_features='log2',min_samples_leaf=10, min_impurity_split=10)

    params = {'max_depth':range(1,20)}  #决策树最大深度
    #params = {'n_neighbors':range(1,20)}
    scoring_fnc = make_scorer(performance_metric)   # 评分函数
    grid = GridSearchCV(regressor,params,cv=cross_validator,scoring=scoring_fnc)

    # 基于输入数据 [x,y],进行网格搜索
    grid = grid.fit(x, y)
    # 返回网格搜索后的最优模型
    return grid.best_estimator_





model = fit_model(train_x,train_y)
def model_imge(model):
    joblib.dump(model,'./keep_model/model.pkl')
    pre_y = model.predict(test_x)
    #计算决策系数r方
    r2 = performance_metric(test_y,pre_y)
    print(r2)
    plt.figure(figsize=(10,9),dpi=100)
    plt.plot(test_y,label='实际值')
    plt.plot(pre_y,label='预测值')
    plt.legend()
    plt.title('实际值与预测值对比')
    plt.show()
model_imge(model)


model_2 = joblib.load('./keep_model/model.pkl')
df_3 = df_2[['房子总面积','套内面积','渝北','江北','沙坪坝','南岸','九龙坡','渝中','巴南','大渡口','北碚','室','厅','厨','卫',' 毛坯 ',' 简装 ',' 精装 ',' 塔楼',' 板楼',' 板塔结合']]
list_x = model_2.predict(df_3)
df_4 = df_2[['价格']]
print('真实价格:',df_4.values,'\n')
print('预测价格:',list_x,'\n')