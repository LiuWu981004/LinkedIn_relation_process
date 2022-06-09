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


def save_json(data_list, path):
    with codecs.open(path, 'w', encoding='utf8') as fw:
        for data in data_list:
            fw.writelines(json.dumps(data, ensure_ascii=False) + "\n")  # writelines必须是str序列


def save_json_single(data, path):
    with codecs.open(path, 'w', encoding='utf8') as fw:
        json.dump(data, fw, ensure_ascii=False)


# mode='a'是在文件结尾加入新写入的内容   会重复写入
def save_json_single_append(data, path):
    with codecs.open(path, mode='a', encoding='utf8') as fw:
        fw.writelines(json.dumps(data, ensure_ascii=False) + "\n")


def read_json(data):
    with open(data, 'r', encoding='utf-8') as f:
        content = json.loads(f.read())
        return content


content_extraction = {'personBaseInfo': 'introduction', 'dynameDetail': 'postingTitle', 'workExperienceDetail': 'duty',
                      'educationDetail': "content", 'volunteerDetail': "description",
                      'recommendationDetail': "recommendationDetails", 'worksDetail': "introduction",
                      'projectsMadeDetail': "projectIntroduction"}


def get_dict_value(in_dict, target_key, results={},
                   not_d=True):  # divided the person_clean_personBaseInfo to different part
    for key in in_dict.keys():  # 迭代当前的字典层级
        data = in_dict[key]  # 将当前字典层级的第一个元素的值赋值给data

        # 如果当前data属于dict类型, 进行回归
        if isinstance(data, dict):
            get_dict_value(data, target_key, results=results, not_d=not_d)
        if isinstance(data, list):
            for data_temp in data:
                get_dict_value(data_temp, target_key, results=results, not_d=not_d)

        # 如果当前键与目标键相等, 并且判断是否要筛选
        if key == target_key and not isinstance(data, dict) and not isinstance(data, list):
            results["text"] = in_dict[key]
            # results.append(in_dict[key])
            if in_dict[key] != "":
                save_json_single_append(results, "../data/LinkedIn_extraction_" + target_key + ".json")
    # return results


def language_detect(data, url):
    print()


"""

def feature_extraction():
    save_dict = {}
    for k,v in data.items():
        save_dict[text]=
        print()
"""

if __name__ == "__main__":
    for key, value in content_extraction.items():
        # print(key,value)
        get_dict_value(read_json("../data/LinkedIn_users_" + key + ".json"), target_key=value, )
        
