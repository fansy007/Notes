#!/usr/bin/env python3
"""
CS500 每日市场评分脚本（含微信推送）
用法：python3 cs500_daily_score.py
收盘后运行，自动计算6项客观指标并推送到微信
"""

import akshare as ak
import numpy as np
import urllib.request
import urllib.parse
import datetime
import ssl
import warnings
warnings.filterwarnings('ignore')

# 忽略SSL证书验证（国内环境常见问题）
ssl_ctx = ssl.create_default_context()
ssl_ctx.check_hostname = False
ssl_ctx.verify_mode = ssl.CERT_NONE

# Server酱 SendKey
SERVERCHAN_KEY = "SCT324772TaxDmd34XqSO0F52XfcN9iNB5"

def send_wechat(title, content):
    """通过Server酱推送到微信"""
    url = f"https://sctapi.ftqq.com/{SERVERCHAN_KEY}.send"
    data = urllib.parse.urlencode({
        "title": title,
        "desp": content
    }).encode("utf-8")
    try:
        req = urllib.request.Request(url, data=data, method="POST")
        with urllib.request.urlopen(req, timeout=10, context=ssl_ctx) as resp:
            result = resp.read().decode()
            if '"code":0' in result:
                print("✅ 微信推送成功")
            else:
                print(f"⚠️ 推送返回: {result}")
    except Exception as e:
        print(f"❌ 微信推送失败: {e}")

def calc_score():
    today_str = datetime.date.today().strftime("%Y-%m-%d")
    # 动态计算日期范围
    start_hist = (datetime.date.today() - datetime.timedelta(days=30)).strftime("%Y%m%d")
    start_week = (datetime.date.today() - datetime.timedelta(days=10)).strftime("%Y%m%d")
    end_date   = datetime.date.today().strftime("%Y%m%d")

    print("正在获取数据...\n")

    # ============ 1. PE历史百分位 ============
    df_pe = ak.stock_index_pe_lg(symbol="中证500")
    today = df_pe.iloc[-1]
    current_pe = today['滚动市盈率']
    current_index = today['指数']
    current_date = str(today['日期'])

    pe_3y = df_pe['滚动市盈率'].iloc[-750:]
    pe_percentile = (pe_3y < current_pe).sum() / len(pe_3y) * 100

    if pe_percentile < 20:
        pe_score, pe_level = 2, "严重低估"
    elif pe_percentile < 40:
        pe_score, pe_level = 1, "低估"
    elif pe_percentile < 60:
        pe_score, pe_level = 0, "合理"
    elif pe_percentile < 80:
        pe_score, pe_level = -1, "偏贵"
    else:
        pe_score, pe_level = -2, "严重高估"

    # ============ 2. 成交量 vs 5日均值 ============
    df_hist = ak.stock_zh_index_hist_csindex(symbol="000905", start_date=start_hist, end_date=end_date)
    vol_5d_avg = df_hist['成交量'].iloc[-6:-1].mean()
    vol_today = df_hist['成交量'].iloc[-1]
    vol_ratio = vol_today / vol_5d_avg

    if vol_ratio > 1.3:
        vol_score = 2
        vol_desc = f"明显放量（{vol_ratio:.1f}x）"
    elif vol_ratio > 0.8:
        vol_score = 0
        vol_desc = f"正常（{vol_ratio:.1f}x）"
    else:
        vol_score = -2
        vol_desc = f"明显缩量（{vol_ratio:.1f}x）"

    # ============ 3. 周级别趋势 vs 沪深300 ============
    df_hs300 = ak.stock_zh_index_hist_csindex(symbol="000300", start_date=start_week, end_date=end_date)
    cs500_week_chg = (df_hist['收盘'].iloc[-1] / df_hist['收盘'].iloc[-6] - 1) * 100
    hs300_week_chg = (df_hs300['收盘'].iloc[-1] / df_hs300['收盘'].iloc[-6] - 1) * 100
    diff = cs500_week_chg - hs300_week_chg

    if diff > 0.5:
        trend_score = 2
        trend_desc = f"跑赢沪深300（CS500:{cs500_week_chg:.1f}% vs HS300:{hs300_week_chg:.1f}%）"
    elif diff > -0.5:
        trend_score = 0
        trend_desc = f"与沪深300持平（CS500:{cs500_week_chg:.1f}% vs HS300:{hs300_week_chg:.1f}%）"
    else:
        trend_score = -2
        trend_desc = f"跑输沪深300（CS500:{cs500_week_chg:.1f}% vs HS300:{hs300_week_chg:.1f}%）"

    # ============ 4. 尾盘表现 ============
    row = df_hist.iloc[-1]
    open_p, high_p, low_p, close_p = row['开盘'], row['最高'], row['最低'], row['收盘']
    close_pos = (close_p - low_p) / (high_p - low_p) * 100 if high_p != low_p else 50

    if close_pos >= 70:
        tail_score = 2
        tail_desc = f"强势收盘（收盘位置{close_pos:.0f}%）"
    elif close_pos >= 40:
        tail_score = 0
        tail_desc = f"中性收盘（收盘位置{close_pos:.0f}%）"
    else:
        tail_score = -2
        tail_desc = f"弱势收盘（收盘位置{close_pos:.0f}%，跌幅{row['涨跌幅']}%）"

    # ============ 5. 融资余额3日变化 ============
    df_rzrq = ak.stock_margin_account_info()
    rzrq_latest = df_rzrq.tail(4)
    rzrq_3d_chg = rzrq_latest['融资余额'].iloc[-1] - rzrq_latest['融资余额'].iloc[-4]

    if rzrq_3d_chg < -100:
        rzrq_score = 2
        rzrq_desc = f"3日净流出{abs(rzrq_3d_chg):.0f}亿（散户撤退，逆向信号）"
    elif rzrq_3d_chg < 100:
        rzrq_score = 0
        rzrq_desc = f"3日基本持平（变化{rzrq_3d_chg:+.0f}亿）"
    else:
        rzrq_score = -2
        rzrq_desc = f"3日净流入{rzrq_3d_chg:.0f}亿（散户追涨，警惕）"

    # ============ 汇总 ============
    total = pe_score + vol_score + trend_score + tail_score + rzrq_score
    cs500_env_score = (total + 10) / 2

    if total >= 8:
        signal = "🔥 强烈看涨"
    elif total >= 3:
        signal = "↗️ 温和看涨"
    elif total >= -2:
        signal = "↔️ 中性震荡"
    elif total >= -7:
        signal = "↘️ 温和看跌"
    else:
        signal = "💧 强烈看跌"

    # ============ 终端输出 ============
    print(f"{'='*52}")
    print(f"  CS500 每日评分  |  {current_date}")
    print(f"{'='*52}")
    print(f"  指数点位: {current_index:.2f}    涨跌幅: {row['涨跌幅']}%")
    print(f"{'='*52}")
    print(f"① PE百分位   {pe_score:+d}分  PE={current_pe:.1f}，3年{pe_percentile:.0f}%分位（{pe_level}）")
    print(f"② 成交量     {vol_score:+d}分  {vol_desc}")
    print(f"③ 周趋势     {trend_score:+d}分  {trend_desc}")
    print(f"④ 尾盘表现   {tail_score:+d}分  {tail_desc}")
    print(f"⑤ 融资余额   {rzrq_score:+d}分  {rzrq_desc}")
    print(f"{'='*52}")
    print(f"  总分: {total:+d} 分    信号: {signal}")
    print(f"  → 五维系统CS500环境分: {cs500_env_score:.1f}分")
    print(f"{'='*52}")

    # ============ 微信推送 ============
    title = f"📊 CS500日报 {current_date} | {total:+d}分 {signal}"
    content = f"""## CS500 每日评分报告

**日期**：{current_date}
**指数点位**：{current_index:.2f}（{row['涨跌幅']}%）

---

| 维度 | 得分 | 说明 |
|------|------|------|
| ① PE百分位 | {pe_score:+d}分 | PE={current_pe:.1f}，3年{pe_percentile:.0f}%分位（{pe_level}） |
| ② 成交量 | {vol_score:+d}分 | {vol_desc} |
| ③ 周趋势 | {trend_score:+d}分 | {trend_desc} |
| ④ 尾盘表现 | {tail_score:+d}分 | {tail_desc} |
| ⑤ 融资余额 | {rzrq_score:+d}分 | {rzrq_desc} |

---

**总分：{total:+d} 分**
**信号：{signal}**
**五维系统CS500环境分：{cs500_env_score:.1f} 分**
"""
    send_wechat(title, content)

if __name__ == "__main__":
    calc_score()
