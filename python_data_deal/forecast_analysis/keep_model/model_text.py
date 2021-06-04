from sklearn.externals import joblib
import pandas as pd



#x1 = ['房子总面积','卫','室','套内面积','厅','江北','渝北','渝中',' 毛坯 ']
# x = [[100,1,3,80,1,0,1,0,0],[120,2,3,108,1,1,0,0,1]]
# data = pd.read_excel(r'C:\Users\chenyao\Desktop\预测数据.xls')
# data[['室','厅','卫']] = data['房屋类型'].str.extract('(\d)室(\d)厅(\d)卫')
# data.drop('房屋类型',axis=1,inplace=True)
# data['室'] = data['室'].astype(float)
# data['厅'] = data['厅'].astype(float)
# data['卫'] = data['卫'].astype(float)
#
# c = pd.get_dummies(data['装修程度'])
# a = pd.get_dummies(data['所属地区'])
# df = pd.concat([data,c,a],axis=1)
# df.drop(columns=['装修程度','所属地区','实际价格'],axis=1,inplace=True)


model = joblib.load('./model.pkl')

#print(model.predict([df.loc[0]]))
