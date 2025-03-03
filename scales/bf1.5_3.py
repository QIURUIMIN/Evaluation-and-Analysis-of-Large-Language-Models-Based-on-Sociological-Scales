#!user/bin/env python3
# -*- coding: gbk -*-


import pandas as pd


def calculate_personality_scores(file_path, output_path):
    # 加载数据
    data = pd.read_excel(file_path)

    # 定义大五人格维度和侧面及其题目索引
    dimensions = {
        "Extraversion": [1, 6, 11, 16, 21, 26, 31, 36, 41, 46, 51, 56],
        "Agreeableness": [2, 7, 12, 17, 22, 27, 32, 37, 42, 47, 52, 57],
        "Conscientiousness": [3, 8, 13, 18, 23, 28, 33, 38, 43, 48, 53, 58],
        "Negative Emotionality": [4, 9, 14, 19, 24, 29, 34, 39, 44, 49, 54, 59],
        "Open-Mindedness": [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60],
        "Sociability": [1, 16, 31, 46],
        "Assertiveness": [6, 21, 36, 51],
        "Energy Level": [11, 26, 41, 56],
        "Compassion": [2, 17, 32, 47],
        "Respectfulness": [7, 22, 37, 52],
        "Trust": [12, 27, 42, 57],
        "Organization": [3, 18, 33, 48],
        "Productiveness": [8, 23, 38, 53],
        "Responsibility": [13, 28, 43, 58],
        "Anxiety": [4, 19, 34, 49],
        "Depression": [9, 24, 39, 54],
        "Emotional Volatility": [14, 29, 44, 59],
        "Intellectual Curiosity": [10, 25, 40, 55],
        "Aesthetic Sensitivity": [5, 20, 35, 50],
        "Creative Imagination": [15, 30, 45, 60]
    }

    # 定义需要反向计分的题目索引
    reverse_indices = [11, 16, 26, 31, 36, 51, 12, 17, 22, 37, 42, 47, 3, 8, 23, 28, 48, 58, 4, 9, 24, 29, 44, 49, 5,
                       25, 30, 45, 50, 55]

    # 执行反向计分
    scores = data['Extracted Number'].copy()
    for index in reverse_indices:
        scores[index - 1] = 6 - scores[index - 1]

    # 计算每个维度和侧面的得分
    dimension_scores = {}
    for dimension, indices in dimensions.items():
        idx = [i - 1 for i in indices]  # 调整索引以适应Python的0开始索引
        dimension_scores[dimension] = scores.iloc[idx].sum()

    # 保存结果到新的Excel文件
    result_df = pd.DataFrame.from_dict(dimension_scores, orient='index', columns=['Total Score'])
    result_df.to_excel(output_path)

    return dimension_scores


# 指定文件路径
input_file_path = 'bigfive_extracted_numbers1.5.xlsx'
output_file_path = 'bigfive_final_numbers1.5.xlsx'
# 计算得分并保存
scores = calculate_personality_scores(input_file_path, output_file_path)
print("Personality and Facet Scores:", scores)