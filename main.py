import tushare as ts
import requests
from datetime import datetime

# ==================== 配置 ====================
PUSHPLUS_TOKEN = "32f3ef50fd6942eea0b568419d091a83"
TAKE_PROFIT = 2.0
STOP_LOSS = -1.5
# ==============================================

def send(title, content):
    try:
        requests.post("http://www.pushplus.plus/send", json={
            "token": PUSHPLUS_TOKEN,
            "title": title,
            "content": content
        }, timeout=10)
    except:
        print("推送失败")

def select():
    df = ts.get_today_all()
    if df.empty:
        return "今日无数据"

    # 高胜率严格条件
    df = df[
        (df['trade'] >= 6) & (df['trade'] <= 30) &
        (df['changepercent'] >= 1.5) & (df['changepercent'] <= 4.5) &
        (df['turnoverratio'] >= 3) & (df['turnoverratio'] <= 10) &
        (df['nmc'] >= 200000) & (df['nmc'] <= 1000000) &  # 20亿~100亿
        (df['settle'] < df['trade']) &  # 收涨，趋势健康
        (~df['code'].str.startswith(('300','688'))) # 可选：避开创业板科创板，更稳
    ].copy()

    # 排序：量价配合优先
    df = df.sort_values(['turnoverratio','volume'], ascending=[False,False]).head(2)

    if len(df) == 0:
        return "✅ 今日无符合高胜率条件标的，空仓休息"

    msg = "📈 14:30 高胜率选股（仅1-2只）\n\n"
    for _, r in df.iterrows():
        msg += f"{r['code']} {r['name']}\n"
        msg += f"价格：{r['trade']:.2f}  涨幅：{r['changepercent']:.1f}%\n"
        msg += f"止盈2% | 止损1.5% | 明日10点前必卖\n\n"
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

    # 14:30 选股
    if 14 <= h <= 15 and 25 <= m <= 35:
        res = select()
        send("今日高胜率选股", res)
        print(res)

    # 09:35 卖出提醒
    elif 9 <= h <= 10 and 30 <= m <= 45:
        tip = sell_tip()
        send("卖出提醒", tip)
        print(tip)

    else:
        print("不在执行时间段")
