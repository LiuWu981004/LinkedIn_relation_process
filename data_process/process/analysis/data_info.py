from pathlib import Path
import json
import pandas as pd

# ##  先将数据取出来
all_texts=[]
with open("../../data/label_data/label_data_duty.json", 'r', encoding='utf8') as f1:
    with open("../../data/label_data/label_data_edu_content.json", 'r', encoding='utf8') as f2:
        for data_duty, data_edu in zip(f1.readlines(), f2.readlines()):
            i = json.loads(data_duty)
            j = json.loads(data_edu)
            all_texts.append(i['text'])
            all_texts.append(j['text'])

print(all_texts)
# print(data_duty)
# print(type(data_duty))
# all_duty = []
# for i in data_duty:
#     i = json.loads(i)
#     all_duty.append(i['text'])
#     # print(all_duty)
# print(len(all_duty))
# unique_duty = set(all_duty)
# print(len(unique_duty))
# unique_duty_list = list(unique_duty)
# print(unique_duty_list)
#     raw_data_users_file = 'person.json'
# users = json.loads(Path(raw_data_users_file).read_text(encoding='utf8'))
# texts = []
# for u in users:
#     user_texts = parse_user(u)
#     texts.extend(user_texts)
#
# print(len(texts))
# uniq_texts = set(texts)
# uniq_texts_list = list(uniq_texts)
#
# print(uniq_texts_list)
#
# print(len(uniq_texts))
#
# num_tok = [len(t.split()) for t in uniq_texts]
#
# import numpy as np
# import matplotlib.pyplot as plt
#
# num_tok = np.asarray(num_tok)
#
# plt.scatter(range(len(num_tok)), num_tok)
# plt.plot(range(len(num_tok)), np.full_like(num_tok, np.mean(num_tok)), label='mean')
# plt.show()
#
# Path(r'D:\PycharmProjects\LinkedIn_relation_process\data_process\data\all-text.txt').write_text('\n'.join(uniq_texts),
#                                                                                                 encoding='utf8')
