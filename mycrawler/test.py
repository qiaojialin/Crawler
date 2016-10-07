import requests
from bs4 import BeautifulSoup



response = requests.get('http://history.xikao.com/person/%E7%8E%8B%E4%BD%A9%E7%91%9C')
soup = BeautifulSoup(response.text, 'html.parser')

# 去掉网页中“活动年表”以后的文字
import re

all_text = soup.find('div', id='article').td.text.strip()
strinfo = re.compile('活动年表.*')
useful_text = strinfo.sub('', all_text)
print(useful_text)