// ��ȡ�û����롢�Ի���ͱ�
const userInput = document.getElementById('user-input');
const conversation = document.getElementById('conversation');
const conversationForm = document.getElementById('conversation-form');

// ����WebSocket����
const socket = new WebSocket('wss://spark-api.xf-yun.com/v3.1/chat');

// WebSocket������ʱ
socket.onopen = function(event) {
    console.log("WebSocket is open now.");
};

// WebSocket������Ϣʱ
socket.onmessage = function(event) {
    // ������������ص����ݸ�ʽ { message: "�ظ�����Ϣ" }
    const data = JSON.parse(event.data);
    appendMessage('bot', data.message);
};

// WebSocket������
socket.onerror = function(event) {
    console.error("WebSocket error observed:", event);
};

// �ύ���¼�����
conversationForm.addEventListener('submit', function(event) {
    event.preventDefault(); // ��ֹ��Ĭ���ύ��Ϊ

    // ��ȡ�û�������ı�
    const userInputText = userInput.value.trim();

    // ����û�����Ϊ�գ��򲻽��д���
    if (!userInputText) {
        return;
    }

    // ���û���Ϣ��ӵ��Ի�����
    appendMessage('user', userInputText);

    // ͨ��WebSocket�������ݵ�������
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            message: userInputText  // ����API��Ҫ�������͵����ݸ�ʽ
        }));
    } else {
        console.log("WebSocket is not open. Can't send messages.");
    }

    // ����û�����
    userInput.value = '';
});

// ����Ϣ��ӵ��Ի����еĺ���
function appendMessage(role, content) {
    const messageElement = document.createElement('p');
    messageElement.textContent = role === 'user' ? `You: ${content}` : `Bot: ${content}`;
    conversation.appendChild(messageElement);
    // �������Ի���ײ�
    conversation.scrollTop = conversation.scrollHeight;
}