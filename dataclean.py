import pandas as pd

#导入数据
datatmsp = pd.read_excel('datatmsp.xls')

#一、数据清理

import missingno as msno
msno.bar(datatmsp.sample(len(datatmsp)),figsize=(10,4))

#删除缺失值过半的列：
half_count = len(datatmsp)/2
datatmsp = datatmsp.dropna(thresh = half_count,axis=1)

#删除重复行：
datatmsp = datatmsp.drop_duplicates()
#只取了 item_loc, raw_title, view_price, view_sales
#这4列数据，主要对 标题、区域、价格、销量 进行分析

#取出4列的数据
data = pd.DataFrame(datatmsp[['item_loc','raw_title','view_price','view_sales']])
data.head() #默认查看前5行数据（与R类似）

#对item_loc列的省份和城市进行拆分：
#生成province列
data['province'] = data.item_loc.apply(lambda x: x.split()[0])
#由于直辖市的省份和城市相同 这里根据字符串长度进行判断：
data['city'] = data.item_loc.apply(lambda x:
                                   x.split()[0] if len(x)<4 else x.split()[1])
#提取view_sales列中的数字得到sales列：
data['sales'] = data.view_sales.apply(lambda x: x.split('人')[0])
data.dtypes #查看各列数据
#转换数据类型 将sales列的数据转换为整型
data['sales'] = data.sales.astype('int')

list_col = ['province','city']
for i in list_col:
    data[i] = data[i].astype('category')

#删除无用的列：
data = data.drop(['item_loc','view_sales'],axis=1)

#二、数据挖掘与分析
title = data.raw_title.values.tolist() #转为list

#对每一个标题进行分词 使用lcut函数

import jieba
title_s = []
for line in title:
    title_cut = jieba.lcut(line)
    title_s.append(title_cut)
#导入停用词表：
stopwords = pd.read_excel('stopwords.xlsx')
stopwords = stopwords.values.tolist()
#剔除停用词：
title_clean = []
for line in title_s:
    line_clean = []
    for word in line:
        if word not in stopwords:
            line_clean.append(word)
    title_clean.append(line_clean)
#进行去重:
title_clean_dist = []
for line in title_clean:
    line_dist = []
    for word in line:
        if word not in line_dist:
            line_dist.append(word)
    title_clean_dist.append(line_dist)
#将title_clean_dist转为一个list：allwords_clean_dist
allwords_clean_dist = []
for line in title_clean_dist:
    for word in line:
        allwords_clean_dist.append(word)

#把列表allwords_clean_dist转为数据框：
df_allwords_clean_dist = pd.DataFrame({'allwords':allwords_clean_dist})

#对过滤 去重的词语进行分类汇总：
word_count = df_allwords_clean_dist.allwords.value_counts().reset_index()
word_count.columns = ['word','count']

from wordcloud import WordCloud
import matplotlib.pyplot as plt
from scipy.misc import imread
plt.figure(figsize=(20,10))
pic = imread("shafa.png") #读取图片自定义词云形状
w_c = WordCloud(font_path="./data/simhei.ttf",
                background_color="white",
                mask=pic,max_font_size=60,margin=1)
wc = w_c.fit_words({x[0]:x[1] for x in word_count.head(100).values})

plt.imshow(wc,interpolation='bilinear')
plt.axis("off")
#plt.show()
#不同关键词word对应的sales之和的统计分析：
import numpy as np
w_s_sum = []
for w in word_count.word:
    i = 0
    s_list = []
    for t in title_clean_dist:
        if w in t:
            s_list.append(data.sales[i])
        i += 1
    w_s_sum.append(sum(s_list)) #list求和
df_w_s_sum = pd.DataFrame({'w_s_sum':w_s_sum})

#把word_count与对应的df_w_s_sum合并为一个表：
df_word_sum = pd.concat([word_count,df_w_s_sum],axis=1,ignore_index=True)
df_word_sum.columns = ['word','count','w_s_sum']
#对表df_word_sum 中的 word 和 w_s_sum 两列数据进行可视化
#取销量排名前30的词语进行绘图
df_word_sum.sort_values('w_s_sum',inplace=True,ascending=True) #升序
df_w_s = df_word_sum.tail(30) #取最大的30行数据

import matplotlib
from matplotlib import pyplot as plt
font = {'family':'SimHei'} #设置字体
matplotlib.rc('font',**font)
index = np.arange(df_w_s.word.size)
plt.figure(figsize=(6,12))
plt.barh(index,df_w_s.w_s_sum,color='blue',align='center',alpha=0.8)
plt.yticks(index,df_w_s.word,fontsize=11)
#添加数据标签:
for y,x in zip(index,df_w_s.w_s_sum):
    plt.text(x,y,'%.0f' %x,ha='left',va='center',fontsize=11)
#plt.show()
#va的参数有'top','bottom','center','baseline'
#ha的参数有'center','right','left'

#商品的价格分布情况分析： 选择价格小于20000的商品
data_p = data[data['view_price']<20000]
plt.figure(figsize=(7,5))
plt.hist(data_p['view_price'],bins=15,color='purple')
plt.xlabel('价格',fontsize=12)
plt.ylabel('商品数量',fontsize=12)
plt.title('不同价格对应的商品数量分布',fontsize=15)
#plt.show()

#商品的销量分布情况分析:选择销量大于100的商品
data_s = data[data['sales']<20000]
plt.figure(figsize=(7,5))
plt.hist(data_s['sales'],bins=20,color='purple') #分20组
plt.xlabel('销量',fontsize=12)
plt.ylabel('商品数量',fontsize=12)
plt.title('不同销量对应的商品数量分布',fontsize=15)
#plt.show()

#不同价格区间的商品的平均销量分布：
data['price'] = data.view_price.astype('int')
#用qcut将price列分为12组
data['group'] = pd.qcut(data.price,12)
df_group = data.group.value_counts().reset_index()
#以group列进行分类求sales的均值：
df_s_g = data[['sales','group']].groupby('group').mean().reset_index()
#绘制柱形图
index = np.arange(df_s_g.group.size)
plt.figure(figsize=(8,4))
plt.bar(index,df_s_g.sales,color='purple')
plt.xticks(index,df_s_g.group,fontsize=11,rotation=30)
plt.xlabel('Group')
plt.ylabel('mean_sales')
plt.title('不同价格区间的商品的平均销量')
#plt.show()

#商品价格对销量的影响分析：
fig,ax = plt.subplots()
ax.scatter(data_p['view_price'],data_p['sales'],color='purple')
ax.set_xlabel('价格')
ax.set_ylabel('销量')
ax.set_title('商品价格对销量的影响')
#plt.show()
#商品价格对销售额的影响分析：
data['GMV'] = data['price']*data['sales']
import seaborn as sns
sns.regplot(x='price',y='GMV',data=data,color='purple')

#不同省份的商品数量分布：
plt.figure(figsize=(8,4))
data.province.value_counts().plot(kind='bar',color='purple')
plt.xticks(rotation=0)
plt.xlabel('省份')
plt.ylabel('数量')
plt.title('不同省份的商品数量分布')
#plt.show()

#不同省份的商品平均销量分布：
pro_sales = data.pivot_table(index='province',values='sales',aggfunc=np.mean)#分类求均值
pro_sales.sort_values('sales',inplace=True,ascending=False)#排序
pro_sales = pro_sales.reset_index() #重设索引
index = np.arange(pro_sales.sales.size)
plt.figure(figsize=(8,4))
plt.bar(index,pro_sales.sales,color='purple')
plt.xticks(index,pro_sales.province,fontsize=11,rotation=0)
plt.xlabel('province')
plt.ylabel('mean_sales')
plt.title('不同省份的商品平均销量分布')
plt.show()

#导出数据
pro_sales.to_excel('pro_sales.xlsx',index=False)
#绘制热力型地图
