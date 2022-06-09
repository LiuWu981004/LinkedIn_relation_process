import codecs
import json
import pandas as pd
from nlp_preprocess import do_preprocess
import requests
from googletrans import Translator
import pandas as pd
import time
from tqdm import tqdm
from nlp_preprocess.do_preprocess import convert_to_simp


def save_json(data_list, path):
    with codecs.open(path, 'w', encoding='utf8') as fw:
        for data in data_list:
            fw.writelines(json.dumps(data, ensure_ascii=False) + "\n")


def remove_repeat(data_path):
    """去重+翻译"""
    save_list = []
    translate_list = []
    with open(data_path, encoding='utf-8', mode='r') as file:
        text_list = file.readlines()
    for text in text_list:
        temp = json.loads(text)['text']
        real_text = temp[0:int(0.5 * len(temp))]
        left_text = temp[int(0.5 * len(temp)):len(temp)]
        if real_text.strip() == left_text.strip():
            save_list.append({'text': real_text})
            translate_list.append(real_text)
        else:
            save_list.append({'text': temp})
            translate_list.append(temp)

    zh_translate = google_trans_api(translate_list)

    pd.DataFrame({'en': translate_list, 'zh': zh_translate}).to_csv("remove_repeat.csv", index=False)
    # save_json(save_list, "remove_repeat.jsonl")


def google_trans_api(translate_list: list):
    trans = Translator(service_urls=['translate.google.cn'])

    trans_text = []
    concat_text = []
    for item in tqdm(translate_list):
        origin_text = item
        try:
            transed = trans.translate(origin_text, src='en', dest='zh-tw')
            time.sleep(0.5)
            trans_text.append(convert_to_simp(transed.text))
            concat_text.append(origin_text + '\n-------------\n' + transed.text)
        except:
            trans_text.append('翻译api错误')

    return trans_text


def tranlate_by_commercial_api(translate_list: list):
    """
    基于商业翻译API进行文本翻译
    :param translate_list:
    :return:
    """
    # todo 获取ass_token 构建header,如果是提供长期服务，或者频繁调用需要改为定时获取
    res = requests.get(url="https://api2.ctcfile.com/oauth/access-token",
                       params={'client_id': 'UvqOGULBzjMIJxRvL7yCUUkDwr5Fr3X6',
                               'client_secret': '2cc17d56-dd4f-ade7-1f5f-000ccec85d7e'})

    ass_token = json.loads(res.text)['access_token']

    ass_token = "Bearer {}".format(ass_token)
    headers = {"authorization": ass_token}

    # 翻译过程
    translate_url = 'https://api2.ctcfile.com/translations/texts'
    input_data = {
        "src_language_type": "zs",
        "tgt_language_type": "en",
        "texts": translate_list,
        "other": ""
    }
    translate_result = requests.post(translate_url, json=input_data, headers=headers)

    zh_translate = json.loads(translate_result.text)['texts']

    return zh_translate


if __name__ == "__main__":
    remove_repeat("duty.json")
