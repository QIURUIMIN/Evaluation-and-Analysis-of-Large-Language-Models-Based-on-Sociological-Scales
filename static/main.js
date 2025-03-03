import * as base64 from 'base-64'
import CryptoJs from 'crypto-js'

let questionInput = document.querySelector("#question");
let sendMsgBtn = document.querySelector("#btn");
let result = document.querySelector("#result");

let requestObj = {
    APPID: '19753d1f',
    APISecret: 'ZTQ1YzVlZWE4OTMyNWMzZDE4NTM5MGQw',
    APIKey: 'd7f2ea35dc77ac94c54b08d5dea11246',
    Uid:"Q",
    sparkResult: ''
}
// ���������Ϣ��ť
sendMsgBtn.addEventListener('click', (e) => {
    sendMsg()
})
// ��������Ϣ���enter������Ϣ
questionInput.addEventListener('keydown', function (event) {
    if (event.key === 'Enter') { sendMsg(); }
});
// ������Ϣ
const sendMsg = async () => {
    // ��ȡ�����ַ
    let myUrl = await getWebsocketUrl();
    // ��ȡ������е�����
    let inputVal = questionInput.value;
    // ÿ�η������� ����һ���µ�websocketqingqiu
    let socket = new WebSocket(myUrl);

    // ����websocket�ĸ��׶��¼� ������Ӧ����
    socket.addEventListener('open', (event) => {
        console.log('�������ӣ���', event);
        // ������Ϣ
        let params = {
            "header": {
                "app_id": requestObj.APPID,
                "uid": "redrun"
            },
            "parameter": {
                "chat": {
                    "domain": "general",
                    "temperature": 0.5,
                    "max_tokens": 1024,
                }
            },
            "payload": {
                "message": {
                    // ������ȡ��������ĵĻش���Ҫ������ÿ�ν���ʷ�ʴ���Ϣһ�𴫸�����ˣ�����ʾ��
                    // ע�⣺text���������content���ݼ�һ���tokens��Ҫ������8192���ڣ����������нϳ��Ի�������Ҫ�ʵ��ü���ʷ��Ϣ
                    "text": [
                        { "role": "user", "content": "����˭" }, //# �û�����ʷ����
                        { "role": "assistant", "content": "����AI����" },  //# AI����ʷ�ش���
                        // ....... ʡ�Ե���ʷ�Ի�
                        { "role": "user", "content": inputVal },  //# ���µ�һ�����⣬�����������ģ���ֻ������һ������
                    ]
                }
            }
        };
        console.log("������Ϣ");
        socket.send(JSON.stringify(params))
    })
    socket.addEventListener('message', (event) => {
        let data = JSON.parse(event.data)
        // console.log('�յ���Ϣ����',data);
        requestObj.sparkResult += data.payload.choices.text[0].content
        if (data.header.code !== 0) {
            console.log("������", data.header.code, ":", data.header.message);
            // ������"�ֶ��ر�����"
            socket.close()
        }
        if (data.header.code === 0) {
            // �Ի��Ѿ����
            if (data.payload.choices.text && data.header.status === 2) {
                requestObj.sparkResult += data.payload.choices.text[0].content;
                setTimeout(() => {
                    // "�Ի���ɣ��ֶ��ر�����"
                    socket.close()
                }, 1000)
            }
        }
        addMsgToTextarea(requestObj.sparkResult);
    })
    socket.addEventListener('close', (event) => {
        console.log('���ӹرգ���', event);
        // �Ի���ɺ�socket��رգ��������¼���д���
        requestObj.sparkResult = requestObj.sparkResult + "&#10;"
        addMsgToTextarea(requestObj.sparkResult);
        // ��������
        questionInput.value = ''
    })
    socket.addEventListener('error', (event) => {
        console.log('���ӷ��ʹ��󣡣�', event);
    })
}
// ��Ȩurl��ַ
const getWebsocketUrl = () => {
    return new Promise((resovle, reject) => {
        let url = "wss://spark-api.xf-yun.com/v3.1/chat";
        let host = "spark-api.xf-yun.com";
        let apiKeyName = "api_key";
        let date = new Date().toGMTString();
        let algorithm = "hmac-sha256"
        let headers = "host date request-line";
        let signatureOrigin = `host: ${host}\ndate: ${date}\nGET /v1.1/chat HTTP/1.1`;
        let signatureSha = CryptoJs.HmacSHA256(signatureOrigin, requestObj.APISecret);
        let signature = CryptoJs.enc.Base64.stringify(signatureSha);

        let authorizationOrigin = `${apiKeyName}="${requestObj.APIKey}", algorithm="${algorithm}", headers="${headers}", signature="${signature}"`;

        let authorization = base64.encode(authorizationOrigin);

        // ���ո����
        url = `${url}?authorization=${authorization}&date=${encodeURI(date)}&host=${host}`;

        resovle(url)
    })
}
/** ����Ϣ��ӵ�textare��
    ��textarea�в�֧��HTML��ǩ��
    ����ʹ��
    ��ǩ���л��С�
    Ҳ����ʹ��\r\n������ת���ַ���

    ҪʹTextarea�е����ݻ��У�����ʹ��&#13;����&#10;�����л��С�
    &#13;��ʾ�س�����&#10;��ʾ���з���
*/
const addMsgToTextarea = (text) => {
    result.innerHTML = text;
}