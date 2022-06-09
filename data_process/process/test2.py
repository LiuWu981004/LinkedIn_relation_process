from googletrans import Translator
import pandas as pd
import json
from tqdm import tqdm
from nlp_preprocess.do_preprocess import convert_to_simp
import time
import codecs

# 读取领英数据json文件
with open('../data/linkedin216.json', 'r', encoding='utf8') as f:
    content = json.loads(f.read())

df = pd.json_normalize(content)

df = df.fillna('[]')


# 读取需要的列的信息

def column_list(keyword):
    get_list = df[keyword].tolist()
    return get_list
    # x2_list = df['workExperienceDetail'].tolist()


# print(x1_list)
# 将pandas中df需要处理的数据列提取出来，然后进行需要的非结构化文本的抽取
def save_json(data_list, path):
    with codecs.open(path, 'w', encoding='utf8') as fw:
        for data in data_list:
            fw.writelines(json.dumps(data, ensure_ascii=False) + "\n")


def data_extract(list, value):
    data_content = []
    for sample_x1 in list:
        if sample_x1:
            for temp in sample_x1:
                # print(temp,type(temp))
                if value in temp:
                    data_content.append(temp[value])
                    # print(data, type(data))
    # for sample_x2 in x2_list:
    #     if sample_x2:
    #         # print(sample_x2)
    #         for temp in sample_x2:
    #             # print(temp,type(temp))
    #             if 'duty' in temp:
    #                 data_duty.append(temp['duty'])
    #                 # print(data_duty, type(data_duty), end='\n' * 3)
    return data_content


def baidu_trans_api(translate_list: list):
    trans = Translator(service_urls=['http://10.1.170.202:10368/trans_list'])
    trans_text = []
    concat_text = []
    input_data={}
    for item in tqdm(translate_list):
        origin_text = item
        try:
            transed = trans.translate(origin_text, src='en', dest='zh-tw')
            # time.sleep(0.5)
            trans_text.append(convert_to_simp(transed.text))
            concat_text.append(origin_text + '\n-------------\n' + transed.text)
        except:
            trans_text.append('翻译api错误')

    return trans_text


def combine_text(list1, list2, value):
    en_list = list1
    zh_list = list2
    assert len(zh_list) == len(en_list)
    save_list_duty = []
    for i in range(len(zh_list)):
        temp = {'text': en_list[i], 'metadata': zh_list[i]}
        save_list_duty.append(temp)
    save_json(save_list_duty, 'linkined_' + value + '.json')
    # pd.DataFrame({'en': list1, 'zh': list2}).to_csv(keyword + '.csv', index=False)
    # data = pd.read_csv(keyword + ".csv")
    # zh_list = data['zh'].tolist()
    # en_list = data['en'].tolist()
    # assert len(zh_list) == len(en_list)
    # save_list_duty = []
    # for i in range(len(zh_list)):
    #     temp = {'text': en_list[i], 'metadata': zh_list[i]}
    #     save_list_duty.append(temp)
    # save_json(save_list_duty, 'new' + keyword + '.json')


content_extraction = {'educationDetail': "content", 'workExperienceDetail': 'duty'}
if __name__ == "__main__":
    for key, value in content_extraction.items():
        x1_list = column_list(key)
        data_content = data_extract(x1_list, value)
        zh_translate_content = baidu_trans_api(data_content)
        # zh_translate_content = google_trans_api(data_content)
        combine_text(data_content, zh_translate_content, key)
    # pd.DataFrame({'en': data_duty, 'zh': zh_translate_duty}).to_csv("duty.csv", index=False)
    # pd.DataFrame({'en': data_content, 'zh': zh_translate_content}).to_csv("content.csv", index=False)
    # data_duty = pd.read_csv("duty.csv")
    # data_content = pd.read_csv("content.csv")
    # zh_list_duty = data_duty['zh'].tolist()
    # en_list_duty = data_duty['en'].tolist()
    # zh_list_content = data_content['zh'].tolist()
    # en_list_content = data_content['en'].tolist()
    #
    # assert len(zh_list_duty) == len(en_list_duty)
    #
    # save_list_duty = []
    #
    # for i in range(len(zh_list_duty)):
    #     temp = {'text': en_list_duty[i], 'metadata': zh_list_duty[i]}
    #
    #     save_list_duty.append(temp)
    # save_json(save_list_duty, 'new_duty.json')

    # assert len(zh_list_content) == len(en_list_content)
    #
    # save_list_content = []
    #
    # for i in range(len(zh_list_content)):
    #     temp = {'text': en_list_content[i], 'metadata': zh_list_content[i]}
    #
    #     save_list_content.append(temp)
    # save_json(save_list_content, 'new_content.json')
