#!user/bin/env python3
# -*- coding: gbk -*-

from sparkai.llm.llm import ChatSparkLLM, ChunkPrintHandler
from sparkai.core.messages import ChatMessage

#�ǻ���֪��ģ��v3��URLֵ�������汾��ģ��URLֵ��ǰ���ĵ���https://www.xfyun.cn/doc/spark/Web.html���鿴
SPARKAI_URL = 'ws://spark-api.xf-yun.com/v3.1/chat'
#�ǻ���֪��ģ�͵�����Կ��Ϣ����ǰ��Ѷ�ɿ���ƽ̨����̨��https://console.xfyun.cn/services/bm35���鿴
SPARKAI_APP_ID = '19753d1f'
SPARKAI_API_SECRET = 'ZTQ1YzVlZWE4OTMyNWMzZDE4NTM5MGQw'
SPARKAI_API_KEY = 'd7f2ea35dc77ac94c54b08d5dea11246'
#�ǻ���֪��ģ��v3��domainֵ�������汾��ģ��domainֵ��ǰ���ĵ���https://www.xfyun.cn/doc/spark/Web.html���鿴
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
# #������Կ��Ϣ�ӿ���̨��ȡ
# appid = "19753d1f"     #��д����̨�л�ȡ�� APPID ��Ϣ
# api_secret = "ZTQ1YzVlZWE4OTMyNWMzZDE4NTM5MGQw"   #��д����̨�л�ȡ�� APISecret ��Ϣ
# api_key ="d7f2ea35dc77ac94c54b08d5dea11246"    #��д����̨�л�ȡ�� APIKey ��Ϣ
#
# #�������ô�ģ�Ͱ汾��Ĭ�ϡ�general/generalv2��
# domain = "generalv3"   # v1.5�汾
# # domain = "generalv2"    # v2.0�汾
#
# #�ƶ˻����ķ����ַ
# Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"  # v1.5�����ĵ�ַ
# # Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0�����ĵ�ַ


