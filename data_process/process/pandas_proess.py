import json
import sys
import codecs
from pathlib import Path

import pandas as pd
from collections import defaultdict

# corpus = defaultdict(list)
#
# corpus['key'].append()

content_extraction = {'personBaseInfo': 'introduction', 'dynameDetail': 'postingTitle', 'workExperienceDetail': 'duty',
                      'educationDetail': "content", 'volunteerDetail': "description",
                      'recommendationDetail': "recommendationDetails", 'worksDetail': "work_introduction",
                      'projectsMadeDetail': "projectIntroduction"}

# frame = pd.read_json('../data/person.json')
# print(frame)


# from nlp_preprocess.do_preprocess import cut_word_en
# from nlp_preprocess.do_preprocess import sentence_split_en
from nltk.tokenize import sent_tokenize

# #
# with open('../data/LinkedIn_extraction_postingTitle.json', 'r', encoding='utf-8') as f:
#     data = f.readlines()
# #
# for text in data:
#     input = json.loads(text)
#     # print(type(input))
#     temp = input['text']
#     print(sent_tokenize(temp), end='\n' * 2)
#     # print(type(sent_tokenize(temp)))
# #     # print(type(temp))
# #     # result = cut_word_en(temp)
# #     result = sentence_split_en(temp)+-

#     print(result, end='\n'*2)
#
# def gen_text_info_list(file):
#     users=json.loads(...)       # array
#     r=[]
#     for u in users:
#         for k1 in :
#             for k2 in :
#                 text= extract(k1,k2)
#                 if isinstance(text, list):
#                     pass
#                 else:
#                     r.append({
#                         'user': u['name'],
#                         "key":k1,
#                         "key2":k2
#                     })
#     return r
#
# def parse_user(json_obj):
#     result = []
#     for k1, k2 in content_extraction.items():
#         v1 = json_obj[k1]
#         if isinstance(v1, dict):
#             if k2 in v1:
#                 text=v1[k2]
#                 assert isinstance(text, str)
#                 text_info={
#                     'user': json_obj['name'],    # todo
#                     'text':text,
#                     'key1':k1,
#                     'key2': k2
#                 }
#                 result.append(text_info)
#         elif isinstance(v1, list):
#             text_infos=[{
#                     'user': json_obj['name'],    # todo
#                     'text':v2[k2],
#                     'key1':k1,
#                     'key2': k2
#                 }  for v2 in v1 if k2 in v2]
#             result.extend(text_infos)
#         else:
#             print(v1)
#             raise ValueError()
#     return result
#
#
#
# def parse_user(json_obj):
#     for k1, k2 in content_extraction.items():
#         v1 = json_obj[k1]
#         if isinstance(v1, dict):
#             if k2 in v1:
#                 text=v1[k2]
#                 assert isinstance(text, str)
#                 text_info={
#                     'user': json_obj['name'],    # todo
#                     'text':text,
#                     'key1':k1,
#                     'key2': k2
#                 }
#                 yield text_info
#         elif isinstance(v1, list):
#             for v2 in v1:
#                 if k2 in v2:
#                     text_info={
#                     'user': json_obj['name'],    # todo
#                     'text':v2[k2],
#                     'key1':k1,
#                     'key2': k2
#                 }
#                     yield text_info
#
#         else:
#             print(v1)
#             raise ValueError()

with open("person.json", "r+", encoding="utf8") as f:
    users = json.loads(f.read())
    # print(content,)
    # print(type(users))


def parse_user(data_list, temp):


    # print(data, type(data), end='\n' * 5)
    for key1, key2 in content_extraction.items():
        value1 = data[key1]
        result = []
        # print(value1, type(value1), key1, end='\n' * 3)

        if isinstance(value1, dict):
            if key2 in value1:
                if value1[key2] != '' and value1[key2] != []:
                    result.append(value1[key2])
                else:
                    result = ['']
            else:
                result = ['']
            temp[key2].append(result)
        elif isinstance(value1, list):
            for value2 in value1:
                if key2 in value2 and value2[key2] != '' and value2[key2] != []:
                    result.append(value2[key2])
                # else:
                #     result = ['']
            if len(value1) == 0:
                result = ['']
            temp[key2].append(result)
    # return temp
    # if isinstance(value1,list):
    #     for key2 in value1['key2']


# for data in users:
# user = json.loads(data)

# users = json.loads(Path('person.json').read_text(encoding='utf8'))
# texts = []
# for u in users:
#     print(u)
#     user_texts = parse_user(u)
#     texts.extend(user_texts)
if __name__ == "__main__":
    users_texts = []
    temp = defaultdict(list)

    for data in users:  # data 是 dict 类型
        # print(type(data))
        # users_process = parse_user(data, temp)
        parse_user(data, temp)

        # print(len(users_process))
        # if not users_process:
        #     continue
        # users_texts.append(users_process)
    # print(users_texts)
    # print(users_texts, end='\n'*5)
    df = pd.DataFrame(data=temp)
    # df.to_csv('pandas2.csv')
    print(df)
