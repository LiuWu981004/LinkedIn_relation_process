import json
from translate import Translator
content_extraction = {'personBaseInfo': 'introduction', 'dynameDetail': 'postingTitle', 'workExperienceDetail': 'duty',
                      'educationDetail': "content", 'volunteerDetail': "description",
                      'recommendationDetail': "recommendationDetails", 'worksDetail': "introduction",
                      'projectsMadeDetail': "projectIntroduction"}


def parse_user(json_obj):
    result = []
    for k1, k2 in content_extraction.items():
        v1 = json_obj[k1]
        if isinstance(v1, dict):
            if k2 in v1:
                result.append(v1[k2])
        elif isinstance(v1, list):
            result.extend([v2[k2] for v2 in v1 if k2 in v2])
        else:
            print(v1)
            raise ValueError()
    return result


from pathlib import Path

raw_data_users_file = 'person.json'
users = json.loads(Path(raw_data_users_file).read_text(encoding='utf8'))
texts = []
for u in users:
    user_texts = parse_user(u)
    texts.extend(user_texts)

print(len(texts))
uniq_texts = set(texts)
uniq_texts_list =list(uniq_texts)




print(uniq_texts_list)

print(len(uniq_texts))

num_tok = [len(t.split()) for t in uniq_texts]

import numpy as np
import matplotlib.pyplot as plt

num_tok = np.asarray(num_tok)

plt.scatter(range(len(num_tok)), num_tok)
plt.plot(range(len(num_tok)), np.full_like(num_tok, np.mean(num_tok)), label='mean')
plt.show()

Path(r'D:\PycharmProjects\LinkedIn_relation_process\data_process\data\all-text.txt').write_text('\n'.join(uniq_texts),
                                                                                                encoding='utf8')
