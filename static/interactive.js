// 获取用户输入、对话框和表单
const userInput = document.getElementById('user-input');
const conversation = document.getElementById('conversation');
const conversationForm = document.getElementById('conversation-form');

// 创建WebSocket连接
const socket = new WebSocket('wss://spark-api.xf-yun.com/v3.1/chat');

// WebSocket打开连接时
socket.onopen = function(event) {
    console.log("WebSocket is open now.");
};

// WebSocket接收消息时
socket.onmessage = function(event) {
    // 假设服务器返回的数据格式 { message: "回复的消息" }
    const data = JSON.parse(event.data);
    appendMessage('bot', data.message);
};

// WebSocket错误处理
socket.onerror = function(event) {
    console.error("WebSocket error observed:", event);
};

// 提交表单事件监听
conversationForm.addEventListener('submit', function(event) {
    event.preventDefault(); // 防止表单默认提交行为

    // 获取用户输入的文本
    const userInputText = userInput.value.trim();

    // 如果用户输入为空，则不进行处理
    if (!userInputText) {
        return;
    }

    // 将用户消息添加到对话框中
    appendMessage('user', userInputText);

    // 通过WebSocket发送数据到服务器
    if (socket.readyState === WebSocket.OPEN) {
        socket.send(JSON.stringify({
            message: userInputText  // 根据API需要调整发送的数据格式
        }));
    } else {
        console.log("WebSocket is not open. Can't send messages.");
    }

    // 清空用户输入
    userInput.value = '';
});

// 将消息添加到对话框中的函数
function appendMessage(role, content) {
    const messageElement = document.createElement('p');
    messageElement.textContent = role === 'user' ? `You: ${content}` : `Bot: ${content}`;
    conversation.appendChild(messageElement);
    // 滚动到对话框底部
    conversation.scrollTop = conversation.scrollHeight;
}