# AI加密货币多智能体专家系统 - 项目架构文档

## 1. 项目总览

项目实现一个多智能体协作的加密货币交易分析与决策系统，参考 PRD：

- 用户输入目标币种（如 `BTC/USDT`）
- 系统完成：
  1. 分析师阶段（技术面、基本面、新闻、社交情绪）
  2. 研究员辩论阶段（看涨与看跌观点）
  3. 交易与风险评估阶段（生成最终交易决策与风险等级）
- 输出结构化 JSON 结果，包含：
  - 趋势方向
  - 入场点、止盈止损点
  - 风险等级与简要分析摘要

---

## 2. 项目目录结构

```
crypto_multiagent/
│
├─ main.py                     # 主入口：执行完整流程
├─ requirements.txt            # 依赖管理（CCXT、Requests、OpenAI等）
│
├─ agents/                     # 智能体总目录
│  │
│  ├─ analysts/                # 分析师团队
│  │   ├─ base.py              # 分析师基础类与工具
│  │   ├─ fundamentals_analyst.py  # 基本面分析师
│  │   ├─ market_analyst.py        # 技术分析师
│  │   ├─ news_analyst.py          # 新闻分析师
│  │   └─ social_media_analyst.py  # 社交媒体分析师
│  │
│  ├─ researchers/             # 研究员团队
│  │   ├─ base.py              # 研究员基础类
│  │   ├─ bull_researcher.py   # 看涨研究员
│  │   └─ bear_researcher.py   # 看跌研究员
│  │
│  ├─ trader/                  # 交易执行
│  │   └─ trader.py            # 交易员
│  │
│  ├─ risk_management/         # 风险管理团队
│  │   ├─ base.py              # 风险评估基础类
│  │   ├─ aggressive_risk.py   # 激进风险评估员
│  │   ├─ neutral_risk.py      # 中性风险评估员
│  │   └─ conservative_risk.py # 保守风险评估员
│  │
│  └─ managers/                # 管理层
│      ├─ base.py              # 管理基础类
│      ├─ research_manager.py  # 研究经理
│      └─ risk_manager.py      # 风险经理
│
├─ data_providers/             # 数据源模块
│  ├─ market_data.py           # 行情数据 (CCXT)
│  ├─ fundamentals.py          # 链上与基本面数据
│  ├─ news_data.py             # 新闻数据 (CryptoPanic)
│  └─ social_data.py           # 社交舆情 (Twitter / Reddit)
│
├─ utils/                      # 工具模块
│  ├─ state.py                 # AgentState 和 AgentMessage 定义
│  ├─ config.py                # 全局配置和API Key
│  └─ logger.py                # 日志与调试工具
│
└─ output/
    └─ results.json            # 输出最终交易决策结果
```

---

## 3. 核心架构设计

### 3.1 智能体基类

所有智能体继承 `BaseAgent`，并实现 `process(state)` 方法：

```python
class BaseAgent:
    def __init__(self, name):
        self.name = name

    def process(self, state):
        """输入当前AgentState，返回更新后的状态"""
        raise NotImplementedError
```

- `state`：由 `AgentState` 统一管理，包括：
  - 当前币种
  - 分析报告
  - 研究共识
  - 初步交易决策
  - 风险评估结果

---

### 3.2 执行流程（单人开发简化版）

**阶段1：并行分析阶段（Analysts）**
1. `Market Analyst` 获取K线和技术指标（RSI/MACD/布林带）
2. `Fundamentals Analyst` 获取CoinGecko或DefiLlama数据
3. `News Analyst` 获取CryptoPanic新闻并做关键词情绪分析
4. `Social Media Analyst` 爬取Reddit/Twitter简易舆情统计

**阶段2：研究辩论阶段（Researchers + Research Manager）**
1. `Research Manager` 收集所有分析报告
2. `Bull Researcher` 生成看涨理由
3. `Bear Researcher` 生成看跌理由
4. `Research Manager` 形成简化研究共识

**阶段3：交易决策阶段（Trader + Risk Management）**
1. `Trader` 依据研究共识和技术分析生成初步交易方案：
   - 趋势方向
   - 入场点、止盈、止损
2. 风险评估团队：
   - 三个风险评估员输出风险等级
   - `Risk Manager` 汇总为最终风险等级
3. 系统输出最终JSON文件

---

## 4. 核心输出格式

最终输出 `results.json` 示例：

```json
{
  "symbol": "BTC/USDT",
  "trend": "bullish",
  "entry_price": 61850,
  "stop_loss": 60900,
  "take_profit": 63500,
  "confidence_score": 0.78,
  "risk_level": "medium",
  "analysis_summary": {
    "fundamental": "BTC活跃地址增长，长期利好",
    "technical": "多周期趋势上行，关键支撑61800",
    "news": "美联储加息暂停，市场情绪回暖",
    "social": "Twitter热度上升，Reddit多头情绪强烈"
  }
}
```

---

## 5. 单人开发迭代计划

1. **阶段1：核心骨架**
   - 完成目录结构与基础类 (`BaseAgent`, `AgentState`)
   - 实现技术分析师模块（CCXT行情+RSI/MACD分析）

2. **阶段2：数据扩展**
   - 实现新闻分析师与社交分析师
   - 完成基本面分析师的CoinGecko数据接入

3. **阶段3：决策逻辑**
   - 实现研究员与研究经理
   - 实现交易员与简单止盈止损策略

4. **阶段4：风险管理与输出**
   - 实现三类风险评估员与风险经理
   - 输出完整JSON文件并记录日志

5. **阶段5（可选）**
   - 增加并行执行与异步数据获取
   - 增加Web界面或CLI菜单
