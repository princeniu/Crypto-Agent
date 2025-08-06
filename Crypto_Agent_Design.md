# AI加密货币多智能体专家系统 - 工程结构与开发设计（支持独立测试）

## 1. 项目目标

- 构建基于多智能体架构的加密货币交易分析系统
- 单人可开发，可迭代扩展为并行智能体协作
- **每个智能体可单独运行与测试**，便于调试与快速验证
- 输出结构化 JSON，包含：
  - 趋势方向
  - 入场点、止盈止损
  - 风险等级与分析摘要

---

## 2. 项目目录结构

```
crypto_multiagent/
│
├─ main.py                     # 主入口：串联所有智能体完成一次完整分析
├─ requirements.txt            # Python依赖清单
│
├─ agents/                     # 智能体模块
│  │
│  ├─ analysts/                # 分析师团队
│  │   ├─ base.py              # 分析师基础类
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
├─ data_providers/             # 数据获取模块（独立可测试）
│  ├─ market_data.py           # 行情数据 (CCXT)
│  ├─ fundamentals.py          # 基本面&链上数据
│  ├─ news_data.py             # 新闻数据 (CryptoPanic)
│  └─ social_data.py           # 社交舆情数据
│
├─ utils/
│  ├─ state.py                 # AgentState与AgentMessage
│  ├─ config.py                # 配置和API Key
│  └─ logger.py                # 日志工具
│
└─ output/
    └─ results.json            # 最终决策输出
```

---

## 3. 核心设计与独立测试策略

### 3.1 BaseAgent

```python
class BaseAgent:
    def __init__(self, name):
        self.name = name

    def process(self, state):
        """处理输入状态并返回更新后的AgentState"""
        raise NotImplementedError
```

### 3.2 AgentState

```python
class AgentState:
    def __init__(self, symbol):
        self.symbol = symbol
        self.analysis_reports = {}
        self.research_consensus = None
        self.trade_decision = None
        self.risk_assessment = None
```

### 3.3 独立测试策略

1. **每个智能体可单独运行**：
   - 每个 `.py` 文件底部提供 `if __name__ == "__main__":` 测试入口
   - 模拟输入 `symbol`，输出自身分析结果
2. **分析师类测试示例**（`market_analyst.py`）：

```python
if __name__ == "__main__":
    from utils.state import AgentState
    state = AgentState("BTC/USDT")
    agent = MarketAnalyst("Market Analyst")
    result = agent.process(state)
    print(result.analysis_reports["technical"])
```
3. **数据提供模块独立测试**
   - 直接运行 `python data_providers/market_data.py` 获取并打印行情数据
4. **集成测试**
   - `main.py` 串联调用所有智能体，输出 JSON 到 `output/results.json`

---

## 4. 执行流程（支持独立调试）

1. **分析师阶段（Analysts）**
   - 顺序调用或异步调用四个分析师
   - 各自生成独立报告写入 `state.analysis_reports`

2. **研究员辩论阶段（Researchers + Research Manager）**
   - `Research Manager` 收集分析报告
   - 看涨与看跌研究员生成理由
   - 形成研究共识 `state.research_consensus`

3. **交易与风险阶段（Trader + Risk Management）**
   - `Trader` 输出初步决策（趋势、入场点、止盈止损）
   - 三类风险评估员计算风险评分
   - `Risk Manager` 汇总形成最终风险等级与交易方案

4. **输出阶段**
   - 将完整决策写入 `results.json`
   - 每个阶段可单独在终端打印调试

---

## 5. 输出示例

```json
{
  "symbol": "BTC/USDT",
  "trend": "bullish",
  "entry_price": 61850,
  "stop_loss": 60900,
  "take_profit": 63500,
  "risk_level": "medium",
  "analysis_summary": {
    "fundamental": "BTC链上活跃地址增加",
    "technical": "RSI>50，多头趋势",
    "news": "市场利好新闻占比高",
    "social": "Twitter多头情绪上升"
  }
}
```

---

## 6. 单人开发迭代与测试流程

1. **阶段1：核心骨架**
   - 建立目录结构与基础类
   - 实现 MarketAnalyst 并完成独立测试

2. **阶段2：分析师扩展**
   - 实现 NewsAnalyst、SocialMediaAnalyst、FundamentalsAnalyst
   - 独立测试数据获取与分析逻辑

3. **阶段3：研究员与管理层**
   - 实现 Bull/BearResearcher 和 ResearchManager
   - 单独输入模拟分析报告，输出共识文本

4. **阶段4：交易与风险管理**
   - 实现 Trader 和三类风险评估员
   - 独立测试每个风险评估模块

5. **阶段5：集成调试**
   - 串联 main.py
   - 输出最终 JSON，完成闭环
