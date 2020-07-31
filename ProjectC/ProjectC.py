from sklearn import preprocessing
from sklearn.preprocessing import LabelEncoder
from sklearn.cluster import KMeans, AgglomerativeClustering
from sklearn.metrics import silhouette_score
from scipy.cluster.hierarchy import dendrogram, ward
import pandas as pd
import matplotlib.pyplot as plt

#数据规范化
def data_normalize(train_x):
	#数据中的字符串数字化
	str_name = ['CarName', 'fueltype', 'aspiration', 'doornumber', 'carbody', 'drivewheel', 'enginelocation', 'enginetype', 'cylindernumber', 'fuelsystem']
	for i in range(len(str_name)):
		le = LabelEncoder()
		train_x[str_name[i]] = le.fit_transform(train_x[str_name[i]])
	# 规范化到 [0,1] 空间
	min_max_scaler = preprocessing.MinMaxScaler()
	train_x = min_max_scaler.fit_transform(train_x)
	return train_x
# K-Means 手肘法：统计不同K取值的误差平方和
def shouzhou(train_x):	
	sse = []
	for k in range(1, 50):
		# kmeans算法
		kmeans = KMeans(n_clusters=k)
		kmeans.fit(train_x)
		# 计算inertia簇内误差平方和
		sse.append(kmeans.inertia_)
	x = range(1, 50)
	plt.xlabel('K')
	plt.ylabel('SSE')
	plt.plot(x, sse, 'o-')
	plt.show()
#轮廓系数
def lunkuo(train_x):
	sc_scores = []
	k_value = []
	for k in range(2, 50):
	    kmeans = KMeans(n_clusters=k)
	    kmeans_model = kmeans.fit(train_x)
	    sc_score = silhouette_score(train_x, kmeans_model.labels_, metric='euclidean')
	    sc_scores.append(sc_score)
	    k_value.append(k)
	plt.xlabel('k')
	plt.ylabel('SCS')
	plt.plot(k_value, sc_scores, '*-')
	plt.show()
### 使用KMeans聚类
def K_Means(train_x, n_cluster, data):
	kmeans = KMeans(n_clusters=n_cluster)
	kmeans.fit(train_x)
	predict_y = kmeans.predict(train_x)
	# 合并聚类结果，插入到原数据中
	result = pd.concat((data, pd.DataFrame(predict_y)), axis=1)
	result.rename({0:u'聚类结果'}, axis=1, inplace=True)
	print(result)
	# 将结果导出到CSV文件中
	result.to_csv("car_result.csv", index=False, encoding='gbk')
### 使用层次聚类
def CengCi(train_x, n_cluster):
	model = AgglomerativeClustering(linkage='ward', n_clusters=n_cluster)
	y = model.fit_predict(train_x)
	print(y)
	linkage_matrix = ward(train_x)
	dendrogram(linkage_matrix)
	plt.show()
def main():
	#数据读取
	data = pd.read_csv('./CarPrice_Assignment.csv')
	train_x = data.iloc[:, 1:]
	#处理数据
	train_data = data_normalize(train_x)
	#选取K值
	shouzhou(train_data)
	lunkuo(train_data)
	#确定K值
	K_Num = int(input('数据聚类的类数为：'))
	#KMeans与层次聚类
	K_Means(train_data, K_Num, data)
	CengCi(train_data, K_Num)
if __name__ == '__main__':
	main()
