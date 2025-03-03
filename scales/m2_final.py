# -*- coding: utf-8 -*-

import pandas as pd

# 读取包含分数的表格
df = pd.read_excel('ENFJ_Extracted_Values.xlsx')

# 计算每个维度的总得分
df['E'] = df.iloc[:, [0, 4, 8, 12, 16, 20, 24, 28, 32, 36, 40, 44]].sum(axis=1)
df['I'] = df.iloc[:, [1, 5, 9, 13, 17, 21, 25, 29, 33, 37, 41, 45]].sum(axis=1)
df['S'] = df.iloc[:, [2, 6, 10, 14, 18, 22, 26, 30, 34, 38, 42, 46]].sum(axis=1)
df['N'] = df.iloc[:, [3, 7, 11, 15, 19, 23, 27, 31, 35, 39, 43, 47]].sum(axis=1)
df['T'] = df.iloc[:, [48, 52, 56, 60, 64, 68, 72, 76, 80, 84, 88, 92]].sum(axis=1)
df['F'] = df.iloc[:, [49, 53, 57, 61, 65, 69, 73, 77, 81, 85, 89, 93]].sum(axis=1)
df['J'] = df.iloc[:, [50, 54, 58, 62, 66, 70, 74, 78, 82, 86, 90, 94]].sum(axis=1)
df['P'] = df.iloc[:, [51, 55, 59, 63, 67, 71, 75, 79, 83, 87, 91, 95]].sum(axis=1)

# 根据每个维度的总得分确定性格类型
df['Personality'] = ''
df.loc[df['E'] > df['I'], 'Personality'] += 'E'
df.loc[df['E'] <= df['I'], 'Personality'] += 'I'
df.loc[df['S'] > df['N'], 'Personality'] += 'S'
df.loc[df['S'] <= df['N'], 'Personality'] += 'N'
df.loc[df['T'] > df['F'], 'Personality'] += 'T'
df.loc[df['T'] <= df['F'], 'Personality'] += 'F'
df.loc[df['J'] > df['P'], 'Personality'] += 'J'
df.loc[df['J'] <= df['P'], 'Personality'] += 'P'

# 输出结果
print(df['Personality'])
