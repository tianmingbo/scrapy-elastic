__author__ = '田明博'
__date__ = '2019/11/27 17:53'
with open(r'C:\Users\asus\Desktop\爬虫\scrapy教程\zhisousou\utils\ip.txt', 'r') as f:
    PROXIES = f.readlines()
PROXIE = []
for i in PROXIES:
    PROXIE.append('http://'+i.replace('\n', ''))
print(PROXIE)
