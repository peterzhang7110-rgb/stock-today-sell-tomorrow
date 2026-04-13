import tushare as ts
import requests
from datetime import datetime

# ==================== 已填好，直接用 ====================
WXPUSHER_APP_TOKEN = "AT_GyAhiy9pYeiyr46sackbNYI7xE6cS5xT"
WXPUSHER_UID = "UID_Xac6nA0jvr8vdaRLKCETavSDHt5v"
TAKE_PROFIT = 2.0
STOP_LOSS = -1.5
# ==========================================================

def send_wechat(title, content):
    url = "https://wxpusher.zjiecode.com/api/send/message"
    data = {
        "appToken": WXPUSHER_APP_TOKEN,
        "content": content,
        "summary": title,
        "contentType": 1,
        "uids": [WXPUSHER_UID]
    }
    try:
        requests.post(url, json=data, timeout=10)
        print("推送成功")
    except Exception as e:
        print(f"推送失败: {e}")

def select():
    df = ts.get_today_all()
    if df.empty:
        return "今日无数据"

    df = df[
        (df['trade'] >= 6) & (df['trade'] <= 30) &
        (df['changepercent'] >= 1.5) & (df['changepercent'] <= 4.5) &
        (df['turnoverratio'] >= 3) & (df['turnoverratio'] <= 10) &
        (df['nmc'] >= 200000) & (df['nmc'] <= 1000000) &
        (df['settle'] < df['trade']) &
        (~df['code'].str.startswith(('300','688')))
    ].copy()

    df = df.sort_values(['turnoverratio','volume'], ascending=[False,False]).head(2)

    if len(df) == 0:
        return "✅ 今日无符合高胜率条件标的，空仓休息"

    msg = "📈 14:30 高胜率选股（仅1-2只）\n\n"
    for _, r in df.iterrows():
        msg += f"{r['code']} {r['name']}\n"
        msg += f"价格：{r['trade']:.2f}  涨幅：{r['changepercent']:.1f}%\n"
        msg += f"✅ 止盈2% | ❌ 止损1.5% | 明日10点前必卖\n\n"
    return msg

def sell_tip():
    tip = "⏰ 明日卖出规则（10点前清仓）\n\n"
    tip += f"• 涨幅 ≥ {TAKE_PROFIT}% → 止盈卖出\n"
    tip += f"• 跌幅 ≤ {STOP_LOSS}% → 止损卖出\n"
    tip += "• 不盈不亏 → 冲高就卖，不格局\n"
    return tip

if __name__ == "__main__":
    now = datetime.now()
    h, m = now.hour, now.minute

    if 14 <= h <= 15 and 25 <= m <= 35:
        res = select()
        send_wechat("今日高胜率选股", res)
        print(res)

    elif 9 <= h <= 10 and 30 <= m <= 45:
        tip = sell_tip()
        send_wechat("卖出提醒", tip)
        print(tip)

    else:
        print("不在执行时间段")
