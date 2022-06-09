#!/usr/bin/python
# -*- coding: UTF-8 -*-
"""
@author: 
@file: 
@time:2
@description: 
"""
# dict_ = {'text': 'I love you', 'trans': '我爱你', 'school': '清华大学', 'location': '深圳市南山区'}
# list_ = ['this is a pen', 'he is taller than me', 'i am a students of china',
#          'Dr. Panchanathan currently serves as the Director of the National Science Foundation (NSF). Although this account will remain live during his tenure, do not expect any direct communications from this account. Please tag NSF’s official LinkedIn page in updates that refer to Dr. Panchanathan in his official capacity as Director of NSF. All media inquiries should be sent to media@nsf.gov. Dr. Sethuraman Panchanathan received his Ph.D. in electrical and computer engineering from the University of Ottawa in 1989. He brought his skills and knowledge to Arizona State University, where he became the founding director of the School of Computing and Informatics, and was instrumental in starting the Biomedical Informatics Department. He also founded the Center for Cognitive Ubiquitous Computing (CUbiC) at ASU, which is focused on developing devices, technologies, and environments for assisting individuals with disabilities. In 2014, Dr. Panchanathan was appointed by United States President Barack Obama to the U.S. National Science Board (NSB). He now chairs the NSB Committee on Strategy and Budget, which oversees an annual budget of $7 billion. He has also been appointed by U.S. Secretary of Commerce, Penny Pritzker, to the National Advisory Council on Innovation and Entrepreneurship (NACIE) to advance the innovation economy and grow a globally competitive workforce. Arizona Secretary of State Michele Reagan appointed him to the Technology, Transparency and Commerce Council in 2016 to provide strategic insight for Arizona’s policy programs. Dr. Panchanathan is a Fellow of the National Academy of Inventors (NAI) and a Fellow of the Canadian Academy of Engineering. He has chaired the Council of Research at Association of Public and Land-grant Universities (APLU). He previously led the Knowledge Enterprise Development at ASU, helping build transdisciplinary research institutes. He has published over 440 highly cited papers in prestigious journals and conferences and obtained numerous patents and copyrights. He is the founder of two start-up companies and is a mentor to numerous researchers and students.']
# # # list_.append(dict_)
# # print(list_)
# rest_dict = dict_.pop('school',)
# rest_dict = dict_.pop('location')
# print(dict_)
# # for i in list:
# #     print(i)
# #     print(type(i))
# if 'text' in dict_:
#     print('yes ,i am right')

# A = []
# B = 'yes ,i am right'
# A.append(B)
# A.extend(B)
# print(A)
# for i in A:
#     print(type(i))
# from collections import defaultdict
#
import json

content_extraction = {'personBaseInfo': ['introduction', 'good', 'nice'], 'dynameDetail': ['postingTitle', ],
                      'workExperienceDetail': 'duty',
                      'educationDetail': "content", 'volunteerDetail': "description",
                      'recommendationDetail': "recommendationDetails", 'worksDetail': "introduction",
                      'projectsMadeDetail': "projectIntroduction"}
# # dict_ = {'text': 'I love you', 'trans': '我爱你', 'school': '清华大学', 'location': '深圳市南山区'}
# # list_ = ['this is a pen', 'he is taller than me', 'i am a students of china',
# # corpus = defaultdict(list)
# # corpus['key'].append()
import pandas as pd
import json

df = pd.DataFrame(content_extraction, index=[1, 2, 3, ])
print(df)
# print(df.fillna(value=0))
for index, row in df.iterrows():
    print(row, type(row))
    for data in row['personBaseInfo']:
        print(data)

# import numpy as np
# import pandas as pd
#
# a = np.arange(100, dtype=float).reshape((10, 10))
# # for i in range(len(a)):
# #     a[i, :i] = np.nan
# # a[6, 0] = 100.0
#
# d = pd.DataFrame(data=a)
# print(d)
