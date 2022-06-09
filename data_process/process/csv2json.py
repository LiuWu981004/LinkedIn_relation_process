import json
import pandas as pd
import codecs


def save_json(data_list, path):
    with codecs.open(path, 'w', encoding='utf8') as fw:
        for data in data_list:
            fw.writelines(json.dumps(data, ensure_ascii=False) + "\n")


data = pd.read_csv("remove_repeat.csv")
zh_list = data['zh'].tolist()
en_list = data['en'].tolist()

assert len(zh_list) == len(en_list)

save_list = []

for i in range(len(zh_list)):
    temp = {'text': en_list[i], 'metadata': zh_list[i]}

    save_list.append(temp)
save_json(save_list, 'duty.json')

#
# def cvs2json(file_path):
#     input_data = []
#     fo = with open(file_path, "r", encoding="utf-8") as f
#     for line in fo:
#         line = line.replace("\n", "")  # 将换行换成空
#         line_arr = line.split(",")
#         while not line_arr[-1].strip():
#             del line_arr[-1]
#         input_data.append(line_arr)  # 以，为分隔符
#     fo.close()  # 关闭文件流

# data = {}
# for row_index in range(len(input_data)):
#     row_data = input_data[row_index]
#     sub_data = data
#     col_len = len(row_data)
#     for col_index in range(col_len):
#         current_data = row_data[col_index]
#         # 判断目标数据是否为空，且是否是最后一个元素
#         if current_data != '':
#             sub_data[current_data] = [{}] if col_index < col_len - 1 else []
#             if len(sub_data[current_data]) > 0:
#                 sub_data = sub_data[current_data][0]
#         else:
#             # 确定上一个条目
#             pre_row_index = row_index
#             while not input_data[pre_row_index][col_index].strip():
#                 pre_row_index -= 1
#             sub_data = sub_data[input_data[pre_row_index][col_index]][0]
# json_data = json.dumps(data, ensure_ascii=False)
# return (json_data)



