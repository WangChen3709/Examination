import pandas as pd
import time
from efficient_apriori import apriori as ap
from mlxtend.frequent_patterns import apriori as apr
from mlxtend.frequent_patterns import association_rules

#数据读取及分析数据提取
file = open('./订单表.csv')
data = pd.read_csv(file)
dataset = data[['客户ID', '产品名称']]
dataset = dataset.drop(dataset[dataset.产品名称 == 'none'].index)
dataset = dataset.sort_values(by='客户ID', ascending=True)

## 采用efficient_apriori工具包
def Rule1():
	start = time.time()
	#设置索引
	order_series = dataset.set_index('客户ID')['产品名称']
	#将产品名称数据按照客户ID且去重后放入transactions中
	transactions = []
	temp_index = 0
	for i,v in order_series.items():
		if i != temp_index:
			temp = set()
			temp_index = i
			temp.add(v)
			transactions.append(temp)
		else:
			temp.add(v)
	#对数据进行关联分析
	itemsets, rules = ap(transactions, min_support=0.01,  min_confidence=0.3)
	print('频繁项集：', itemsets)
	print('关联规则：', rules)
	end = time.time()
	print("用时：", end-start)

#采用mlxtend.frequent_patterns工具包
def Rule2():
	start = time.time()
	#将产品名称数据按客户ID分类且去重后放入字典中
	order_series = dataset.set_index('客户ID')['产品名称']
	temp_user = {}
	temp_index = 0
	for i,v in order_series.items():
		if i != temp_index:
			temp_index = i
			temp_user[i] = v
		else:
			if temp_user[i].find(v) == -1:
				temp_user[i] += '|'+v
	#将字典中的数据转化为DataFrame格式
	analysis_data = pd.DataFrame([temp_user])
	analysis_data=analysis_data.T
	analysis_data.columns = ['产品名称']
	#将数据进行hot_encoded编码
	analysis_data_hot_encoded = analysis_data.drop('产品名称', 1).join(analysis_data.产品名称.str.get_dummies('|'))
	#对数据进行关联分析
	itemsets = apr(analysis_data_hot_encoded, use_colnames=True, min_support=0.05)
	# 按照支持度从大到小进行排序
	itemsets = itemsets.sort_values(by="support" , ascending=False) 
	print('-'*20, '频繁项集', '-'*20)
	print(itemsets)
	# 根据频繁项集计算关联规则，设置最小提升度为2
	rules =  association_rules(itemsets, metric='lift', min_threshold=1)
	# 按照提升度从大到小进行排序
	rules = rules.sort_values(by="lift" , ascending=False) 
	print('-'*20, '关联规则', '-'*20)
	print(rules)
	end = time.time()
	print("用时：", end-start)
	
def main():
	Rule1()
	Rule2()

if __name__ == '__main__':
	main()
