#!user/bin/env python3
# -*- coding: gbk -*-

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

#星火认知大模型v3的URL值，其他版本大模型URL值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_URL = 'ws://spark-api.xf-yun.com/v3.1/chat'
#星火认知大模型调用秘钥信息，请前往讯飞开放平台控制台（https://console.xfyun.cn/services/bm35）查看
SPARKAI_APP_ID = '19753d1f'
SPARKAI_API_SECRET = 'ZTQ1YzVlZWE4OTMyNWMzZDE4NTM5MGQw'
SPARKAI_API_KEY = 'd7f2ea35dc77ac94c54b08d5dea11246'
#星火认知大模型v3的domain值，其他版本大模型domain值请前往文档（https://www.xfyun.cn/doc/spark/Web.html）查看
SPARKAI_DOMAIN = 'generalv3'

def api(question, model):
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(
        role="user",
        content=question
    )]
    handler = ChunkPrintHandler()
    a = spark.generate([messages], callbacks=[handler])
    return a.generations[0][0].text




# import SparkApi
# #以下密钥信息从控制台获取
# appid = "19753d1f"     #填写控制台中获取的 APPID 信息
# api_secret = "ZTQ1YzVlZWE4OTMyNWMzZDE4NTM5MGQw"   #填写控制台中获取的 APISecret 信息
# api_key ="d7f2ea35dc77ac94c54b08d5dea11246"    #填写控制台中获取的 APIKey 信息
#
# #用于配置大模型版本，默认“general/generalv2”
# domain = "generalv3"   # v1.5版本
# # domain = "generalv2"    # v2.0版本
#
# #云端环境的服务地址
# Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v1.5环境的地址
# # Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址


