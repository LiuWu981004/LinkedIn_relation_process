#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: 
@file: 
@time:2
@description: 
"""
import json
import codecs


# 定义保存json文件函数
def save_json_single(data, path):
    with codecs.open(path, 'w', encoding='utf8') as fw:
        json.dump(data, fw, ensure_ascii=False)


# 定义读取json文件函数
def read_json(data):
    with open(data, 'r', encoding='UTF-8') as f:
        data_content = json.loads(f.read())
        return data_content


# 关键字列表
list_extraction = ['personBaseInfo', 'dynameDetail', 'workExperienceDetail', 'educationDetail', 'volunteerDetail',
                   'recommendationDetail', 'worksDetail', 'projectsMadeDetail']


def extract_key(key: str, data):  # can solve a particular problem to satisfy our demand
    index = 0
    save_dict = {}
    for i in data:
        # print(dict{key: i[key]})
        # print(dict((k, i[k]) for k in list_extraction))
        save_dict[index] = {key: i[key]}
        index += 1
    save_json_single(save_dict, "../data/LinkedIn_users_" + key + ".json")


if __name__ == "__main__":
    for key in list_extraction:  # use the way of 'for' to call function extract_key
        extract_key(key, read_json("../data/LinkedIn_users.json"))  # 给入文件地址
        # get_dict_value(read_json("../data/LinkedIn_users_" + key + ".json"), target_key='value', )

    # for key, value in content_extraction.items():
    #     get_dict_value(read_json("../data/LinkedIn_users_" + key + ".json"), target_key='introduction', )
