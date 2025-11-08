import requests
from flask import Flask, request

app = Flask(__name__)

# ========== 共用配置 ==========
OPENAI_API_KEY = "sk-xxx"  # 你的K2 API Key
BASE_URL = "https://api.moonshot.cn/v1"
MODEL = "kimi-k2-latest"
# ==============================

# 刀哥配置
DAOGE_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx1"  # 刀哥机器人地址
# 阿发配置
AFU_WEBHOOK = "https://open.feishu.cn/open-apis/bot/v2/hook/xxx2"    # 阿发机器人地址

def call_k2(messages):
    """调用K2模型的通用函数"""
    response = requests.post(
        f"{BASE_URL}/chat/completions",
        headers={"Authorization": f"Bearer {OPENAI_API_KEY}"},
        json={"model": MODEL, "messages": messages}
    ).json()
    return response['choices'][0]['message']['content']

# ========== 刀哥路由 ==========
@app.route("/", methods=['POST'])
def daoge_reply():
    data = request.json
    message = data.get('text', '')
    
    # 刀哥prompt
    system_prompt = "你是刀哥，专怼阿发，每次回复必须否定他并给出落地动作，语气凶狠，回复控制在100字内"
    
    reply_text = call_k2([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ])
    
    # 回飞书并@阿发
    requests.post(DAOGE_WEBHOOK, json={
        "msg_type": "text",
        "content": {"text": f"@阿发 {reply_text}"}
    })
    
    return "OK"

# ========== 阿发路由 ==========
@app.route("/afu", methods=['POST'])
def afu_reply():
    data = request.json
    message = data.get('text', '')
    
    # 阿发prompt
    system_prompt = "你是阿发，专笑刀哥格局小，每次提供3个剑走偏锋的脑洞，回复控制在100字内"
    
    reply_text = call_k2([
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": message}
    ])
    
    # 回飞书并@刀哥
    requests.post(AFU_WEBHOOK, json={
        "msg_type": "text",
        "content": {"text": f"@刀哥 {reply_text}"}
    })
    
    return "OK"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=80)
