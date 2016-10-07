import requests
from bs4 import BeautifulSoup
try:
    import xml.etree.cElementTree as ET
except ImportError:
    import xml.etree.ElementTree as ET

base_url = 'http://history.xikao.com'
response = requests.get(base_url + '/people')
soup = BeautifulSoup(response.text, 'html.parser')

a_family_array = soup.find('div', id='article').ul.findAll('a')
#存放每个演员名字和网址的dict
name_url = dict()
#演员总数
peopleNum = 0
dis_num = 0
#遍历所有姓氏
for a_family in a_family_array:
    response = requests.get(base_url + a_family['href'])
    soup = BeautifulSoup(response.text, 'html.parser')

    #得到所有演员的a标签
    a_name_array = soup.find('div', id='article').findAll('a')

    #遍历所有演员
    for a_name in a_name_array:
        name_url[a_name['title']] = base_url + a_name['href']
        peopleNum += 1
        print(a_name['title'], base_url + a_name['href'])

xml_name_root = ET.Element('people')
xml_people_root = ET.Element('people')

count = 0

for name in name_url:
    person_abs_url = name_url[name]
    # 将所有演员姓名保存到xml中
    xml_name = ET.SubElement(xml_name_root, 'name')
    xml_name.text = name

    if count <= 1000:
        # 将演员姓名，url，介绍放在xml中
        response = requests.get(person_abs_url)
        soup = BeautifulSoup(response.text, 'html.parser')
        xml_person = ET.SubElement(xml_people_root, 'person')
        xml_name = ET.SubElement(xml_person, 'name')
        xml_name.text = name
        xml_url = ET.SubElement(xml_person, 'url')
        xml_url.text = person_abs_url
        xml_dis = ET.SubElement(xml_person, 'dis')

        # 去掉网页中“活动年表”以后的文字
        import re
        try:
            all_text = soup.find('div', id='article').table.text.strip()
            useful_text = re.compile('活动年表.*').sub('', all_text)
            xml_dis.text = useful_text
            count += 1
            print('抓取了第', count, '个演员', name, '的信息')
        except:
          pass

tree_name = ET.ElementTree(xml_name_root)
f = open('E:/name.xml', 'wb')
tree_name.write(f)
f.close()

tree_people = ET.ElementTree(xml_people_root)
f = open('E:/discription.xml', 'wb')
tree_people.write(f)
f.close()