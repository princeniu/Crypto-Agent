# AI Crypto Multi-Agent System

一个基于多智能体的加密货币分析和交易决策系统。

## 项目概述

本项目实现了一个多智能体系统，用于加密货币市场分析、风险评估和交易决策。系统包含多个专业智能体，每个智能体负责特定的分析领域，通过协作提供全面的投资建议。

## 系统架构

### 智能体团队

#### 分析师团队 (Analysts)
- **市场分析师** (`market_analyst.md`) - 技术分析和市场趋势
- **基本面分析师** (`fundamentals_analyst.md`) - 基本面分析
- **新闻分析师** (`news_analyst.md`) - 新闻和事件分析
- **社交媒体分析师** (`social_media_analyst.md`) - 社交媒体情绪分析

#### 研究员团队 (Researchers)
- **多头研究员** (`bull_researcher.md`) - 看涨观点研究
- **空头研究员** (`bear_researcher.md`) - 看跌观点研究

#### 风险管理团队 (Risk Management)
- **激进辩论者** (`aggresive_debator.md`) - 高风险策略
- **保守辩论者** (`conservative_debator.md`) - 低风险策略
- **中性辩论者** (`neutral_debator.md`) - 平衡策略

#### 交易员团队 (Trader)
- **交易员** (`trader.md`) - 执行交易决策

#### 管理层 (Managers)
- **研究经理** (`research_manager.md`) - 协调研究活动
- **风险管理经理** (`risk_manager.md`) - 风险管理协调

## 项目文档

- [产品需求文档](Crypto_Agent_PRD.md) - 详细的产品需求和功能规范
- [系统架构文档](Crypto_Agent_Architecture.md) - 技术架构和系统设计
- [设计测试文档](Crypto_Agent_Design.md) - 测试策略和独立测试设计

## 开发规范

### 文件结构
```
agents/
├── analysts/          # 分析师智能体
├── researchers/       # 研究员智能体
├── risk_management/   # 风险管理智能体
├── trader/           # 交易员智能体
└── managers/         # 管理层智能体
```

### 开发要求
- 每个智能体必须可独立运行测试
- 使用 `AgentState` 或字典传递状态
- 输出结果保存到 `output/results.json`
- 遵循模块化、可测试的设计原则

## 使用方法

1. 克隆仓库
```bash
git clone https://github.com/princeniu/Crypto-Agent.git
cd Crypto-Agent
```

2. 安装依赖
```bash
pip install -r requirements.txt
```

3. 运行独立测试
```bash
python agents/analysts/market_analyst.py
```

## 输出格式

系统输出包含以下字段：
- `symbol`: 交易对符号
- `trend`: 市场趋势 (bullish/bearish/neutral)
- `entry_price`: 入场价格
- `stop_loss`: 止损价格
- `take_profit`: 止盈价格
- `risk_level`: 风险等级
- `analysis_summary`: 分析摘要

## 贡献指南

1. Fork 项目
2. 创建功能分支
3. 提交更改
4. 推送到分支
5. 创建 Pull Request

## 许可证

MIT License

## 联系方式

如有问题或建议，请通过 GitHub Issues 联系。 