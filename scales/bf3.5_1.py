#!user/bin/env python3
# -*- coding: gbk -*-


import pandas as pd
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

# �ǻ���֪��ģ�͵�URL��API��Կ��������
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.5/chat'
SPARKAI_APP_ID = '19753d1f'
SPARKAI_API_SECRET = 'ZTQ1YzVlZWE4OTMyNWMzZDE4NTM5MGQw'
SPARKAI_API_KEY = 'd7f2ea35dc77ac94c54b08d5dea11246'
SPARKAI_DOMAIN = 'generalv3.5'


# ��ȡExcel�ļ�
def read_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df['Question'].tolist()


# ������ʹ𰸱��浽�µ�Excel�ļ�
def save_to_excel(questions, responses, output_file):
    df = pd.DataFrame({
        'Question': questions,
        'Response': responses
    })
    df.to_excel(output_file, index=False)


# ����������б��Excel�ļ��ж�ȡ
file_path = 'C:\\Users\\14542\\Desktop\\MProject\\scales\\bigfive.xlsx'
descriptions = read_questions_from_excel(file_path)


def generate_responses(spark, descriptions):
    handler = ChunkPrintHandler()
    responses = []

    rating_instruction = "���ÿ�����ӻظ���Ӧ�������Ա�����ͬ���ͬ�����������1���ǳ���ͬ�⡢2����̫ͬ�⡢3��̬��������4���Ƚ�ͬ�⡢5���ǳ�ͬ�⡣��ֻ��Ҫ�ظ�һ�����֡�"

    for description in descriptions:
        full_message = f"{rating_instruction} {description}"
        messages = [ChatMessage(role="user", content=full_message)]
        response = spark.generate([messages], callbacks=[handler])
        responses.append(response)

    return responses


if __name__ == '__main__':
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )

    responses = generate_responses(spark, descriptions)
    output_file = 'C:\\Users\\14542\\Desktop\\MProject\\scales\\bigfive_responses3.5.xlsx'
    save_to_excel(descriptions, responses, output_file)
    print("Responses have been saved to Excel.")