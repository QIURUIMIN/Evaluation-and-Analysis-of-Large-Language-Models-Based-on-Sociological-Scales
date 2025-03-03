import pandas as pd
from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

# 星火认知大模型的URL，API密钥和域配置
SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.1/chat'
SPARKAI_APP_ID = '19753d1f'
SPARKAI_API_SECRET = 'ZTQ1YzVlZWE4OTMyNWMzZDE4NTM5MGQw'
SPARKAI_API_KEY = 'd7f2ea35dc77ac94c54b08d5dea11246'
SPARKAI_DOMAIN = 'generalv3'


# 读取Excel文件
def read_questions_from_excel(file_path):
    df = pd.read_excel(file_path)
    return df['Question'].tolist()


# 将问题和答案保存到新的Excel文件
def save_to_excel(questions, responses, output_file):
    df = pd.DataFrame({
        'Question': questions,
        'Response': responses
    })
    df.to_excel(output_file, index=False)


# 描述性语句列表从Excel文件中读取
file_path = 'C:\\Users\\14542\\Desktop\\MProject\\scales\\bigfive.xlsx'
descriptions = read_questions_from_excel(file_path)


def generate_responses(spark, descriptions):
    handler = ChunkPrintHandler()
    responses = []

    rating_instruction = "请对每个句子回复对应的数字以表明你同意或不同意这个描述，1：非常不同意、2：不太同意、3：态度中立、4：比较同意、5：非常同意。你只需要回复一个数字。"

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
    output_file = 'C:\\Users\\14542\\Desktop\\MProject\\scales\\bigfive_responses.xlsx'
    save_to_excel(descriptions, responses, output_file)
    print("Responses have been saved to Excel.")





