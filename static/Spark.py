from flask import Flask, render_template
from flask_socketio import SocketIO, emit
from sparkai.llm.llm import ChatSparkLLM
from sparkai.core.messages import ChatMessage

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)

SPARKAI_URL = 'wss://spark-api.xf-yun.com/v3.1/chat'
SPARKAI_APP_ID = '19753d1f'
SPARKAI_API_SECRET = 'ZTQ1YzVlZWE4OTMyNWMzZDE4NTM5MGQw'
SPARKAI_API_KEY = 'd7f2ea35dc77ac94c54b08d5dea11246'
SPARKAI_DOMAIN = 'generalv3'

def call_spark_ai(question):
    # 设置你的聊天机器人配置
    spark = ChatSparkLLM(
        spark_api_url=SPARKAI_URL,
        spark_app_id=SPARKAI_APP_ID,
        spark_api_key=SPARKAI_API_KEY,
        spark_api_secret=SPARKAI_API_SECRET,
        spark_llm_domain=SPARKAI_DOMAIN,
        streaming=False,
    )
    messages = [ChatMessage(role="user", content=question)]
    handler = ChunkPrintHandler()  # 确保ChunkPrintHandler适用于你的需求
    spark.generate([messages], callbacks=[handler])
    return handler.output  # 返回结果，确保output是正确的属性

@app.route('/')
def index():
    return render_template('index.html')  # 确保你有一个index.html文件

@socketio.on('send_message')
def handle_message(data):
    question = data['message']
    answer = call_spark_ai(question)
    emit('receive_message', {'message': answer})

if __name__ == '__main__':
    socketio.run(app, debug=True)