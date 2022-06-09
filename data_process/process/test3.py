# # import json
# # import pandas as pd
# #
# # # data = {
# # #     "state": "Florida",
# # #     "shortname": "FL",
# # #     "info": {"governor": "Rick Scott"},
# # #     "counties": [
# # #         {"name": "Dade", "population": 12345},
# # #         {"name": "Broward", "population": 40000},
# # #         {"name": "Palm Beach", "population": 60000},
# # #     ],
# # # }
# # # lis2 = ['i', 'kdas ', 'qew ', 'qe q', 'qwde ']
# # #
# #
# # # print(lis2.text)
# # # result = pd.json_normalize(data, 'counties', ['state', 'shortname', ['info', 'governor']])
# # # # print(type(result))
# # # for index, row in result.iteritems():
# # #     temp = row[1]
# # #     print(temp,type(temp))
# # # with open('LinkedIn_extraction_duty.json', encoding='utf-8', mode='r') as file:
# # #     text_list = file.readlines()
# # # for text in text_list:
# # #     temp = json.loads(text)['text']
# # #     print(type(temp),temp,end='\n'*3)
# # # def test_return(lis2):
# # #     n1 = lis2[0]
# # #     n2 = lis2[2]
# # #     return n2, n1
# # #
# # #
# # # data1, data2 = test_return(lis2)
# # # print(data1, data2)
# # from googletrans import Translator
# import pandas as pd
# import json
# #
# #
# #
# # # 读取领英数据json文件
# # with open('person.json', 'r', encoding='utf8') as f:
# #     content = json.loads(f.read())
# #
# # df = pd.json_normalize(content)
# # df.info()
# # # print(df)
# import requests
#
# # URL = 'http://raw.githubusercontent.com/BindiChen/machine-learning/master/data-analysis/027-pandas-convert-json/data/simple.json'
# # data = requests.get(URL)
# # print(type(data))
# # # data = json.loads(requests.get(URL).text)
# # # df =pd.json_normalize(data)
# # # print(df)
# json_list = [
#     {
#         'class': 'Year 1',
#         'student count': 20,
#         'room': 'Yellow',
#         'info': {
#             'teachers': {
#                 'math': 'Rick Scott',
#                 'physics': 'Elon Mask'
#             }
#         },
#         'students': [
#             {
#                 'name': 'Tom',
#                 'sex': 'M',
#                 'grades': {'math': 66, 'physics': 77}
#             },
#             {
#                 'name': 'James',
#                 'sex': 'M',
#                 'grades': {'math': 80, 'physics': 78}
#             },
#         ]
#     },
#     {
#         'class': 'Year 2',
#         'student count': 25,
#         'room': 'Blue',
#         'info': {
#             'teachers': {
#                 'math': 'Alan Turing',
#                 'physics': 'Albert Einstein'
#             }
#         },
#         'students': [
#             {'name': 'Tony', 'sex': 'M'},
#             {'name': 'Jacqueline', 'sex': 'F'},
#         ]
#     },
# ]
# df = pd.json_normalize(json_list, record_path=['students'], meta=['class', 'room'],record_prefix='students.')
# # print(df)
#
# ints_list = [1, 2, 3, 4, 3, 2]
#
# # ints_list2 = list(dict.fromkeys(ints_list))
# ints_list2 = dict.fromkeys(ints_list)
# print(ints_list2)  # [1, 2, 3, 4]
list1 = ['1', '2', '3']
list2 = ['4', '5', '6']
for i, j in zip(list1, list2):
    print(i, end='\n' * 3)
    print(j, end='\n' * 3)
