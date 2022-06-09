# 将给的数据去重，
import json
import pandas as pd
import requests
import codecs
from tqdm import tqdm

#  读取文件的函数
def read_json(path):
    with open(path, 'r', encoding='utf8') as f:
        data = f.readlines()
        return data


def save_json(data_list, path):
    with codecs.open(path, 'w', encoding='utf8') as fw:
        for data in data_list:
            fw.writelines(json.dumps(data, ensure_ascii=False) + "\n")


# 去除两个list中重复的部分
def repeat_remove(list_old, list_new):
    all_sent_old = []
    all_sent_new = []
    all_sent =[]

    for item in list_old:
        all_sent_old.append(json.loads(item)['text'])
    for item in list_new:
        all_sent_new.append(json.loads(item)['text'])
    for item in all_sent_new:
        if item not in all_sent_old:
            all_sent.append(item)
    all_unique_sent = list(set(all_sent))
    all_unique_sent.sort(key=all_sent.index)
    return all_unique_sent


def tran(sent_list):
    zh_trans_list = []
    en_data = {"data": sent_list}
    url = 'http://10.1.170.202:10368/trans_list'
    print('going to translation,it have over 200 sentences, please wait!!!')
    zh_trans = requests.post(url, json=en_data)
    zh_trans = zh_trans.json()
    for zh in tqdm(zh_trans):
        for i in zh['trans_result']:
            zh_trans_list.append(i['dst'])
    return zh_trans_list


def combine_en_zh(en_list, zh_list):
    assert len(zh_list) == len(en_list)
    save_list = []
    for i in range(len(zh_list)):
        temp = {'text': en_list[i], 'metadata': zh_list[i]}
        save_list.append(temp)
    save_json(save_list, 'new_duty.json')


if __name__ == '__main__':
    content_label = read_json('../data/old_workExperienceDetail-duty.json')
    content_new = read_json('../data/new_duty.json')
    result = repeat_remove(content_label, content_new)
    print(result)
    print(len(result), type(result))
    zh_trans_list = tran(result)
    print(zh_trans_list, len(zh_trans_list))
    combine_en_zh(result, zh_trans_list)
