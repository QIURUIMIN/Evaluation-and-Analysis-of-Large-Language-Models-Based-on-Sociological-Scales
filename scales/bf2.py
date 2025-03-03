#!user/bin/env python3
# -*- coding: gbk -*-

import pandas as pd
import re

def read_responses_and_extract_numbers(file_path):
    # ��ȡExcel�ļ�
    df = pd.read_excel(file_path)

    # ȷ��Response��Question�д���
    if 'Response' not in df.columns or 'Question' not in df.columns:
        print("Required columns are not found in the Excel file.")
        return None

    # ��ȡÿ��response�е�����
    extracted_numbers = []
    pattern = re.compile(r"generations=\[\[ChatGeneration\(text='(\d+)'")

    for response in df['Response']:
        match = pattern.search(str(response))
        if match:
            number = match.group(1)
            extracted_numbers.append(number)
        else:
            extracted_numbers.append("No number found")

    # �����µ�DataFrame
    result_df = pd.DataFrame({
        'Question': df['Question'],
        'Extracted Number': extracted_numbers
    })
    return result_df

def save_to_excel(df, output_file):
    # ��DataFrame���浽Excel
    df.to_excel(output_file, index=False)

# ���������ļ�·��
input_file_path = 'C:\\Users\\14542\\Desktop\\MProject\\scales\\bigfive_responses.xlsx'
output_file_path = 'C:\\Users\\14542\\Desktop\\MProject\\scales\\bigfive_extracted_numbers.xlsx'

# ��ȡ�ʹ�������
result_df = read_responses_and_extract_numbers(input_file_path)
if result_df is not None:
    save_to_excel(result_df, output_file_path)
    print("Data has been saved to the new Excel file.")
else:
    print("Data processing failed.")