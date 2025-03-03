#!user/bin/env python3
# -*- coding: gbk -*-

import pandas as pd
import re

def read_responses_and_extract_numbers(file_path):
    # 读取Excel文件
    df = pd.read_excel(file_path)

    # 确保Response和Question列存在
    if 'Response' not in df.columns or 'Question' not in df.columns:
        print("Required columns are not found in the Excel file.")
        return None

    # 提取每个response中的数字
    extracted_numbers = []
    pattern = re.compile(r"generations=\[\[ChatGeneration\(text='(\d+)'")

    for response in df['Response']:
        match = pattern.search(str(response))
        if match:
            number = match.group(1)
            extracted_numbers.append(number)
        else:
            extracted_numbers.append("No number found")

    # 创建新的DataFrame
    result_df = pd.DataFrame({
        'Question': df['Question'],
        'Extracted Number': extracted_numbers
    })
    return result_df

def save_to_excel(df, output_file):
    # 将DataFrame保存到Excel
    df.to_excel(output_file, index=False)

# 输入和输出文件路径
input_file_path = 'C:\\Users\\14542\\Desktop\\MProject\\scales\\bigfive_responses.xlsx'
output_file_path = 'C:\\Users\\14542\\Desktop\\MProject\\scales\\bigfive_extracted_numbers.xlsx'

# 读取和处理数据
result_df = read_responses_and_extract_numbers(input_file_path)
if result_df is not None:
    save_to_excel(result_df, output_file_path)
    print("Data has been saved to the new Excel file.")
else:
    print("Data processing failed.")