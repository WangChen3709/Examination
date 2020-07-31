from bs4 import BeautifulSoup
import requests
import pandas as pd
import re
from lxml import etree

#定义待爬取数据网址
url='http://car.bitauto.com/xuanchegongju/?l=8&mid=8'
#读取网页数据
def page_content(url):
	header = {'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11 '}
	response = requests.get(url, headers=header, timeout=10)
	return response
#对网页数据进行分析
def analysis_data(response):
	#定义所需要的临时变量
	baojia_page_1 = pd.DataFrame(columns=['照片链接'])
	baojia_page_2 = pd.DataFrame(columns=['名称', '最低价格（万元）', '最高价格（万元）'])
	temp = {}
	temp2 = {}
    	#提取照片链接B
	imglink = {}
	#读取当前网页所有照片链接
	imglink = re.findall(r'class="img" src="(.*?)"', response.text)
	#对照片链接进行处理
	for num in range(0,len(imglink)):
		temp['照片链接'] = 'http:'+str(imglink[num])
		baojia_page_1 = baojia_page_1.append(temp, ignore_index=True)
	#提取名称与价格
	Soup = BeautifulSoup(response.text, 'html.parser')
	#提取名称与价格所在class内容
	temp_data = Soup.find('div', class_="search-result-list")
	#提取各车型名称与价格的分支数据
	car_list = temp_data.find_all('a')
	#将数据各名称及对应的价格提取并保存到DataFrame中
	for car in car_list:
		car_data_list = car.find_all('p')
		if car_data_list[1].text != '暂无':
			temp2['名称'] = car_data_list[0].text
			price_list = car_data_list[1].text.split('-')
			temp2['最低价格（万元）'] = price_list[0]
			temp2['最高价格（万元）'] = price_list[1].replace('万','')
		else:
			temp2['名称'] = car_data_list[0].text
			temp2['最低价格（万元）'] = '暂无'
			temp2['最高价格（万元）'] = '暂无'
		baojia_page_2=baojia_page_2.append(temp2, ignore_index=True)
	#将照片链接与名称价格的DataFrame合并
	baojia_page = pd.concat([baojia_page_2, baojia_page_1], axis=1)
	return baojia_page
		
	
def main():
	Response = page_content(url)
	BaoJia_Page = analysis_data(Response)
	BaoJia_Page.to_csv('BaoJia_Page.csv', index=False, encoding='gbk')
	

if __name__ == '__main__':
	main()
