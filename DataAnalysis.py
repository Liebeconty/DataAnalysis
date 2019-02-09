import pandas as pd
#数据导入
jobdata = pd.read_excel('testdata.xls')

import missingno as msno
import re
import math

#数据清理
msno.bar(jobdata.sample(len(jobdata)),figsize=(10,4))
#删除缺失值超过一半的列
half_count = len(jobdata)/2
jobdata = jobdata.dropna(thresh=half_count,axis=1)
#删除缺失值过多的行
jobdata = jobdata.dropna(axis=0)
data_job = jobdata.drop_duplicates()
#取出需要分析的列
data = pd.DataFrame(data_job[['职位名','公司名','工作地点','薪资']])

#数据整理
data['city'] = data.工作地点.apply(lambda x: x.split('-')[0])
#data['position'] = data.职位名.apply(lambda x: x.split()[0])
data['position'] = data['职位名']
data['company'] = data['公司名']
#re.match(r'(\d+|\d+(\.\d+))-(\d+|\d+(\.\d+))千/月','18.50-19千/月')
data['salary'] = data.薪资.apply(lambda x:
                               str(float(x.split('千')[0].split('-')[0]))
                               +'-'+
                               str(float(x.split('千')[0].split('-')[1]))
                               if re.match(r'(\d+|\d+(\.\d+))-(\d+|\d+(\.\d+))千/月',x) else x)
#x元/天 一个月取20天
data['salary'] = data.salary.apply(lambda x:
                               str(float(x.split('元')[0])*20/1000)
                               if re.match(r'(\d+|\d+(\.\d+))元/天',x) else x)
data['salary'] = data.salary.apply(lambda x:
                               str(float(x.split('万')[0].split('-')[0])*10)
                               +'-'+
                               str(float(x.split('万')[0].split('-')[1])*10)
                               if re.match(r'(\d+|\d+(\.\d+))-(\d+|\d+(\.\d+))万/月',x) else x)
data['salary'] = data.salary.apply(lambda x:
                               str(math.floor(float(x.split('万')[0].split('-')[0])*10/12))
                               +'-'+
                               str(math.floor(float(x.split('万')[0].split('-')[1])*10/12))
                               if re.match(r'(\d+|\d+(\.\d+))-(\d+|\d+(\.\d+))万/年',x) else x)
data['salary'] = data.salary.apply(lambda x:
                               str(float(x.split('万以上')[0])*10)
                               if re.match(r'(\d+|\d+(\.\d+))万以上/月',x) else x)
data['salary'] = data.salary.apply(lambda x:
                               str(float(x.split('万以')[0])*10/12)
                               if re.match(r'(\d+|\d+(\.\d+))万以(上|下)/年',x) else x)
data['salary'] = data.salary.apply(lambda x:
                               str(float(x.split('千以下')[0]))
                               if re.match(r'(\d+|\d+(\.\d+))千以下/月',x) else x)
#最小薪资 元/月
data['Minsalary'] = data.salary.apply(lambda x:
                                    float(x.split('-')[0])
                                    if re.match(r'(\d+|\d+(\.\d+))-(\d+|\d+(\.\d+))',x) else float(x))
#最大薪资 元/月
data['Maxsalary'] = data.salary.apply(lambda x:
                                    float(x.split('-')[1])
                                    if re.match(r'(\d+|\d+(\.\d+))-(\d+|\d+(\.\d+))',x) else float(x))
#删除无用的列
data = data.drop(['职位名','公司名','工作地点','薪资','salary'],axis=1)

#数据分析

#描述性统计分析
#招聘岗位最多的30个城市
#因招聘城市未知，去除异地招聘
city = data['city'].value_counts()[:31].drop('异地招聘').reset_index()
"""
#平均薪资（上限、下限）
salary = data.groupby(['city'])['Minsalary','Maxsalary'].mean().reset_index()
salary = salary.sort_values('Maxsalary',ascending=False) #降序排列
#最高、最低薪资
Msalary = data.groupby('city').agg({'Minsalary':'min','Maxsalary':'max'})
"""
#计算各公司招聘岗位平均工资
data['salary'] = (data['Maxsalary'] + data['Minsalary'])/2
#分省份求最高、最低平均工资 取前30
salary = data.groupby('city')['salary'].agg(['max','min']).reset_index()
salary = salary.sort_values('max',ascending=False)[:31] #降序排列
t=list(salary.city)
t.remove('异地招聘')
salary = salary[salary.city.isin(t)]
from matplotlib import pyplot as plt
plt.figure(figsize=(8,4))
plt.bar(salary['city'],salary['max'],color='blue')
plt.xticks(rotation=0)
plt.xlabel('城市')
plt.ylabel('薪资')
plt.title('各城市薪资分布/K')
#plt.show()


plt.figure(figsize=(8,4))
plt.bar(city['index'],city['city'],color='blue')
plt.xticks(rotation=0)
plt.xlabel('城市')
plt.ylabel('岗位数')
plt.title('各城市招聘岗位数')
plt.show()

