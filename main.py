import requests

# 你的WxPusher信息（已填好，直接用）
WXPUSHER_APP_TOKEN = "AT_GyAhiy9pYeiyr46sackbNYI7xE6cS5xT"
WXPUSHER_UID = "UID_Xac6nA0jvr8vdaRLKCETavSDHt5v"

def send_test():
    url = "https://wxpusher.zjiecode.com/api/send/message"
    data = {
        "appToken": WXPUSHER_APP_TOKEN,
        "content": "✅ 测试消息！GitHub推送成功！",
        "summary": "测试推送",
        "contentType": 1,
        "uids": [WXPUSHER_UID]
    }
    try:
        resp = requests.post(url, json=data, timeout=10)
        print(f"推送返回结果: {resp.text}")
        print("推送请求已发送，请查看微信和WxPusher日志")
    except Exception as e:
        print(f"推送失败: {e}")

if __name__ == "__main__":
    send_test()
