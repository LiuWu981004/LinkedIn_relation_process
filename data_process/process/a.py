s = '''LinkedIn_extraction_content.json
LinkedIn_extraction_description.json
LinkedIn_extraction_duty.json
LinkedIn_extraction_introduction.json
LinkedIn_extraction_postingTitle.json
LinkedIn_extraction_projectIntroduction.json
LinkedIn_extraction_recommendationDetails.json'''
files = s.splitlines(keepends=False)

import json
from pathlib import Path

texts = []
for file in files:
    print(file)

    for line in Path(r'D:\PycharmProjects\LinkedIn_relation_process\data_process\data', file).read_text(
            encoding='utf8').splitlines(keepends=False):
        text = json.loads(line)['text']
        texts.append(text)

print(len(texts))

rm_dup_texts = set(texts)
print(len(rm_dup_texts))
