import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import tushare as ts

'''
#获取数据
s_pf = '600000'
s_gd = '601818'
sdate = '2017-01-01'
edate = '2017-12-31'
df_pf = ts.get_h_data(s_pf,start=sdate,end=edate).sort_index(axis=0,ascending=True)
df_gd = ts.get_h_data(s_gd,start=sdate,end=edate).sort_index(axis=0,ascending=True)
df = pd.concat([df_pf.close,df_gd.close],axis=1,keys=['pf_close','gd_close'])
df.ffill(axis=0,inplace=True) #填充数据
df.to_csv('pf_gd.csv')
'''
df = pd.read_csv('pf_gd.csv')

#相关性
corr = df.corr(method='pearson',min_periods=1)
print(corr)
df.plot(figsize=(20,12))
plt.savefig('pf_gd.jpg')
plt.close()

df['pf_one'] = df.pf_close / float(df.pf_close[0]) * 100
df['gd_one'] = df.gd_close / float(df.gd_close[0]) * 100
df.pf_one.plot(figsize=(20,12))
df.gd_one.plot(figsize=(20,12))
plt.savefig('pf_gd_one.jpg')
plt.close()

