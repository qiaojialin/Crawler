# -*- coding: utf-8 -*-
import re
import sys
import jieba
import jieba.posseg as pseg
import os.path

def test(path):
    jieba.load_userdict("dict.txt")
    #存放所有关系
    relations = set()
    #存放所有人名-介绍
    docs = dict()
    for parent, dirs, files in os.walk(path):
        for file in files:
            name = str(file.title()).split('.')[0]
            file_path = os.path.join(parent, file.title())
            text = open(file_path).read()
            docs[name] = text
        for name, dis in docs.items():
            # 删除作品名
            text = re.sub(r'《.*》', '', str(dis))
            sentences = re.split("[.]|[!?]+|[。]|[！？]+|[，]", text)

            pattern_teacher = re.compile(r'.*师从.*|.*从师.*|.*向.*学.*|.*受教于.*|.*拜.*|.*老师.*|' +
                                         '.*被.*收为.*|.*传授.*|.*为师.*|.*得.*真传.*|.*为.*弟子.*|.*受.*指导.*')

            pattern_student = re.compile(r'.*收.*为.*|.*学员.*|.*培养了.*')

            for sentence in sentences:

                match = pattern_teacher.match(sentence)
                if match:
                    print("此句话中有师傅", sentence)
                    words = pseg.cut(sentence)
                    try:
                        for w in words:
                            if len(w.word) == 1 or len(w.word) == 4:
                                continue
                            if str(w.flag) == "nr":
                                relations.add(w.word + " " + "师徒" + " " + name + "\n")
                    except:
                        pass

                match = pattern_student.match(sentence)
                if match:
                    print("此句话中有徒弟", sentence)
                    words = pseg.cut(sentence)
                    try:
                        for w in words:
                            if len(w.word) == 1 or len(w.word) == 4:
                                continue
                            if str(w.flag) == "nr":
                                relations.add(name + " " + "师徒" + " " + w.word + "\n")
                    except:
                        pass

    f = open('师徒关系抽取.txt', 'w+', encoding="UTF-8")
    f.writelines(relations)
    f.close()

if __name__ == '__main__':
    test(sys.argv[1])

