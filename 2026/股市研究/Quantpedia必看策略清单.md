# Quantpedia 必看策略清单

> 学习路径：理论 → 原理 → 代码实现
> 目标：深入理解突破回踩、缩量整理等形态的本质

---

## 第一阶段：均值回归（Mean Reversion）

### 1. Short-Term Reversal
- **核心逻辑**：短期过度反应后会回归均值
- **关键词**：1-month reversal, short-term contrarian
- **为什么有效**：投资者过度反应、流动性压力
- **失效条件**：强趋势市场、高波动期
- **学习重点**：
  - 怎么定义"短期"
  - 用什么指标判断"过度反应"
  - 回测结果在不同市场的差异

### 2. Pullback Trading
- **核心逻辑**：趋势中的健康回调是买入机会
- **关键词**：trend pullback, retracement
- **为什么有效**：趋势延续需要洗盘、获利回吐
- **失效条件**：趋势反转、假突破
- **学习重点**：
  - 怎么区分回调和反转
  - 回调深度的量化标准
  - 再启动信号的确认

### 3. RSI Mean Reversion
- **核心逻辑**：RSI超买超卖后的回归
- **关键词**：RSI(2), RSI(14), oversold bounce
- **为什么有效**：情绪极端后的修复
- **失效条件**：趋势太强、持续超买/超卖
- **学习重点**：
  - RSI参数的选择
  - 超买超卖阈值的设定
  - 和其他指标的结合

---

## 第二阶段：突破（Breakout）

### 4. Breakout with Volume
- **核心逻辑**：放量突破才是真突破
- **关键词**：volume confirmation, breakout validation
- **为什么有效**：成交量代表资金共识
- **失效条件**：假突破、诱多
- **学习重点**：
  - 放量的量化标准（几倍均量？）
  - 突破后回踩的概率
  - 如何过滤假突破

### 5. Channel Breakout
- **核心逻辑**：价格通道上下轨的突破
- **关键词**：trading range, support resistance
- **为什么有效**：通道代表供需平衡，突破代表失衡
- **失效条件**：通道太窄、震荡市
- **学习重点**：
  - 通道怎么构建（时间窗口？）
  - 突破后的目标位计算
  - 止损位设置

### 6. Donchian Channel
- **核心逻辑**：突破N日高低点即开仓
- **关键词**：turtle trading, trend following
- **为什么有效**：趋势跟踪的经典实现
- **失效条件**：震荡市、假突破多
- **学习重点**：
  - N日的选择（20日？50日？）
  - 和趋势强度的关系
  - 海龟交易法则的完整逻辑

---

## 第三阶段：成交量分析（Volume-Based）

### 7. Volume-Price Trend (VPT)
- **核心逻辑**：成交量加权的价格趋势
- **关键词**：volume confirmation, price momentum
- **为什么有效**：量价配合才是真趋势
- **学习重点**：
  - VPT指标的计算
  - 和OBV的区别
  - 背离信号的判断

### 8. Volume Spread Analysis (VSA)
- **核心逻辑**：通过K线形态+成交量判断主力意图
- **关键词**：effort vs result, accumulation distribution
- **为什么有效**：成交量暴露大资金行为
- **学习重点**：
  - 各种K线形态的含义
  - 缩量、放量的不同场景
  - 吸筹、派发的识别

### 9. On-Balance Volume (OBV)
- **核心逻辑**：累计成交量判断资金流向
- **关键词**：money flow, accumulation
- **为什么有效**：资金持续流入推高价格
- **学习重点**：
  - OBV的计算方法
  - OBV背离的判断
  - 和价格的领先滞后关系

---

## 第四阶段：综合策略

### 10. Combined Pullback-Breakout
- **核心逻辑**：趋势突破后的缩量回踩 = 最佳买点
- **关键词**：breakout pullback, trend continuation
- **为什么有效**：结合突破的动量和回调的安全边际
- **学习重点**：
  - 突破强度的判断
  - 回调深度的优化
  - 再启动信号的确认

---

## 学习建议

### 每周安排
| 周次 | 学习内容 | 产出 |
|------|----------|------|
| 第1周 | Short-Term Reversal + Pullback Trading | 笔记：原理、失效条件 |
| 第2周 | Breakout with Volume + Channel Breakout | 笔记：突破确认方法 |
| 第3周 | VPT + VSA + OBV | 笔记：成交量分析方法 |
| 第4周 | Combined Pullback-Breakout | 笔记：整合思路 |

### 笔记模板
```
## 策略名称

### 核心逻辑
- 

### 量化定义
- 

### 为什么有效
- 

### 失效条件
- 

### 和我的研究的关系
- 

### 疑问
- 
```

### 下一步
理解原理后，用 Python 复现策略，用自己的股票数据验证。

---

**最后更新**：2026-03-20
