# -*- coding: utf-8 -*-

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage
import pandas as pd
import re

# 星火认知大模型配置
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.1/chat'
SPARKAI_APP_ID = '19753d1f'
SPARKAI_API_SECRET = 'ZTQ1YzVlZWE4OTMyNWMzZDE4NTM5MGQw'
SPARKAI_API_KEY = 'd7f2ea35dc77ac94c54b08d5dea11246'
SPARKAI_DOMAIN = 'generalv3'

def generate_response(question):
    """使用星火认知大模型生成答案"""
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    intro_message = "istj特征如下1.严肃、安静、藉由集中心 志与全力投入、及可被信赖获致成功。 2.行事务实、有序、实际 、 逻辑、真实及可信赖 3.十分留意且乐于任何事（工作、居家、生活均有良好组织及有序。 4.负责任。5.照设定成效来作出决策且不畏阻挠与闲言会坚定为之。 6.重视传统与忠诚。 7.传统性的思考者或经理。 请阅读题目，并从istj的角度对A、B选项赋值，两项的和等于5，输出两个值，并在20字内说明理由。输出格式如下例如 A:1分 B:3分 理由：...."
    combined_message = intro_message + " 题目: " + question
    messages = [ChatMessage(role="user", content=combined_message)]
    handler = ChunkPrintHandler()
    response = spark.generate([messages], callbacks=[handler])
    print("Response Object:", response)  # 打印响应对象以查看其结构
    return response

def process_questions(input_file, output_file):
    """读取问题，使用星火大模型，保存模型的响应结果"""
    df = pd.read_excel(input_file)

    df = df.fillna('')

    # 合并三列为一个问题，使用A.和B.作为连接符
    df['Combined Question'] = df.iloc[:, 0] + " A. " + df.iloc[:, 1] + " B. " + df.iloc[:, 2]
    print(df['Combined Question'])
    df['Model Response'] = df['Combined Question'].apply(generate_response)
    df.to_excel(output_file, index=False)

def find_first_and_second_numbers(s):
    # 使用正则表达式查找数字
    numbers = re.findall(r'\d+\.\d+|\d+', s)

    if len(numbers) >= 2:
        first_number = float(numbers[0])  # 使用float()将字符串转换为浮点数
        second_number = float(numbers[1])
        return first_number, second_number
    else:
        return None, None


def process_scored_answers(input_file, output_file):
    """从 'Model Response' 列中提取 A 和 B 的值，并保存到文件"""
    df = pd.read_excel(input_file)
    for i in range(len(df['Model Response'])):
        string = df['Model Response'][i]
        # 调用函数
        first, second = find_first_and_second_numbers(string)

        df = pd.read_excel(input_file)
        # 提取 A 和 B 的值
        df[['Value A', 'Value B']] = df['Model Response'].apply(lambda x: pd.Series(find_first_and_second_numbers(x)))

        print("A:", first)
        print("B:", second)

        # 删除 'Option A Score' 和 'Option B Score' 列
        df.drop(columns=['Option A Score', 'Option B Score'], inplace=True)

        # 保存到文件
        df.to_excel(output_file, index=False)


def extract_text(response_string):
    # 使用正则表达式提取 'text' 字段中的内容
    match = re.search(r"text='([^']*)'", response_string)
    if match:
        return match.group(1)
    else:
        return None

def modify_excel_file(input_file):
    # 读取 Excel 文件
    df = pd.read_excel(input_file)

    # 提取 'text' 字段中的内容
    df['Model Response'] = df['Model Response'].apply(extract_text)

    # 保存回同一文件
    df.to_excel(input_file, index=False)

if __name__ == '__main__':
    input_file = 'MBTI_Q.xlsx'  # 输入Excel文件的路径
    output_file = 'Scored_Answers3.xlsx'  # 输出Excel文件的路径
    process_questions(input_file, output_file)
    input_file = 'Scored_Answers3.xlsx'  # 输入Excel文件的路径
    output_file = 'Extracted_Values2.xlsx'  # 输出Excel文件的路径
    process_scored_answers(input_file, output_file)
    input_file = 'C:/Users/14542/Desktop/MProject/scales/Extracted_Values2.xlsx'  # 输入Excel文件的路径
    modify_excel_file(input_file)