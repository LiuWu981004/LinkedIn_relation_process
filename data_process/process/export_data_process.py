#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: 
@file: 
@time:2
@description: 将中文翻译加入到metadata中，按照doccano所需要的格式输入数据
"""
import json
import jsonlines
from pathlib import Path
import codecs

# def parse(self, response):
#     jsonresponse = json.loads(response.text)
#     with jsonlines.open('output.jsonl', mode='a') as writer:
#         writer.write(jsonresponse)

#
with open("../data/all.jsonl", "r+", encoding="utf8") as f:
    # print(f.readlines())
    content = f.readlines()
    # print(type(content))


def save_json(data_list, path):
    with codecs.open(path, 'w', encoding='utf8') as fw:
        for data in data_list:
            fw.writelines(json.dumps(data, ensure_ascii=False) + "\n")


# 保存jsonlines文件
# def parse( response):
#     jsonresponse = json.dumps(response)
#     print(1111,jsonresponse)
#     with jsonlines.open('output.jsonl', mode='a') as writer:
#         writer.write(jsonresponse)


def change_json(data):
    result = []
    # empty_dict={}
    for i in data:
        # print(i)
        # print(type(i))
        data_dict_line = json.loads(i)  # 将字符串变成dict
        temp_text_dict = data_dict_line['text']  # 将dict对应键值对取出来

        split_list = temp_text_dict.split('\n中文翻译：\n')  # 分成列表
        en_text = split_list[0]  # 取出列表中对应元素，类型是  str
        cn_text = split_list[1]
        data_dict_line['text'] = en_text
        data_dict_line['metadata'] = cn_text
        # for key in data_dict_line.keys():
        #     if key =='text' or key =='metadata':
        #         empty_dict[key] = data_dict_line[key]
        result.append(data_dict_line)
    return result
    # return data_dict_line

    # print(78, type(en_text))
    # print(64, cn_text)

    # print(5, type(split_list))
    # print(666, split_list)
    # print(1, temp_dict)
    #
    # print(2, type(temp_dict))


if __name__ == "__main__":
    save_json(change_json(content), 'all_users.jsonl')
    # parse(change_json(content))
#     # for item in jsonlines.Reader(f):
#     #     print(item)
# def process_jsonl(data):
#     for

# 把整个文档读成了字符串，然后把中间分开，使得各个部分不断连接，要改变处理方式。
# content = Path(r'D:\PycharmProjects\LinkedIn_relation_process\data_process\data\all.jsonl').read_text(encoding="utf8")
# data = content.split('\\n中文翻译：\\n')
# # print(data,end='.....')
#
# for i in data:
#     print(i,end='                                 ')
