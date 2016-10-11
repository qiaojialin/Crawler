# -*- coding: utf-8 -*-
from xml.etree import ElementTree
import re
import jieba
import jieba.posseg as pseg

jieba.load_userdict("dict.txt")

#读root
read_root = ElementTree.parse(r"爬虫.xml")
persons = read_root.getiterator("person")

#写root
write_root =ElementTree.Element("documents")

for person in persons:
    refers = set()
    xml_doc = ElementTree.SubElement(write_root, "doc")
    name = person.find("name").text
    dis = person.find("dis").text
    refers.add(name)
    xml_doc.set("name", name)
    # s删除作品名
    text = re.sub(r'《.*》', '', str(dis))
    words = pseg.cut(text)
    try:
        for w in words:
            if len(w.word) == 1 or len(w.word) == 4:
                continue
            if str(w.flag) == "nr":
                refers.add(w.word)
    except:
        pass
    # 去除本人的名字
    refers.remove(name)
    for refer in refers:
        xml_refer = ElementTree.SubElement(xml_doc, "refer")
        xml_refer.text = refer

tree = ElementTree.ElementTree(write_root)
f = open('命名实体识别.xml', 'wb')
tree.write(f)
f.close()



