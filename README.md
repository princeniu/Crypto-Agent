# AI加密货币多智能体专家系统

基于Python的多智能体加密货币交易分析与决策系统，通过不同角色的AI智能体协作完成多维度、多周期市场分析，并辅助用户进行交易决策。

## 🎯 项目特点

- **多智能体架构**：分析师、研究员、管理层协作
- **多维度分析**：技术面、基本面、新闻、社交情绪
- **结构化辩论**：看涨与看跌研究员辩论
- **独立测试**：每个智能体可单独运行测试
- **免费API优先**：使用CCXT、CoinGecko等免费数据源

## 📁 项目结构

```
crypto_multiagent/
├─ main.py                     # 主入口：执行完整流程
├─ test_system.py              # 系统测试脚本
├─ requirements.txt            # Python依赖清单
├─ env_example.txt            # 环境变量示例
│
├─ agents/                     # 智能体模块
│  ├─ analysts/                # 分析师团队
│  │   ├─ base.py              # 分析师基础类
│  │   ├─ market_analyst.py    # 技术分析师
│  │   ├─ fundamentals_analyst.py  # 基本面分析师
│  │   ├─ news_analyst.py      # 新闻分析师
│  │   └─ social_media_analyst.py  # 社交媒体分析师
│  │
│  ├─ researchers/             # 研究员团队
│  │   ├─ base.py              # 研究员基础类
│  │   ├─ bull_researcher.py   # 看涨研究员
│  │   └─ bear_researcher.py   # 看跌研究员
│  │
│  └─ managers/                # 管理层
│      ├─ base.py              # 管理基础类
│      └─ research_manager.py  # 研究经理
│
├─ data_providers/             # 数据获取模块
│  ├─ market_data.py           # 行情数据 (CCXT)
│  ├─ fundamentals.py          # 基本面&链上数据
│  ├─ news_data.py             # 新闻数据 (CryptoPanic)
│  └─ social_data.py           # 社交舆情数据
│
├─ utils/                      # 工具模块
│  ├─ state.py                 # AgentState和AgentMessage
│  ├─ config.py                # 配置和API Key
│  └─ logger.py                # 日志工具
│
└─ output/
    └─ results.json            # 最终决策输出
```

## 🚀 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

复制 `env_example.txt` 为 `.env` 并配置你的API密钥：

```bash
cp env_example.txt .env
```

编辑 `.env` 文件，至少需要配置：
```bash
OPENAI_API_KEY=your_openai_api_key_here
```

### 3. 运行系统测试

```bash
python test_system.py
```

### 4. 运行完整分析

```bash
python main.py
```

## 📊 分析流程

### 阶段1：分析师团队并行分析
- **技术分析师**：基于K线数据和技术指标分析
- **基本面分析师**：基于CoinGecko等链上数据分析
- **新闻分析师**：基于CryptoPanic等新闻数据分析
- **社交媒体分析师**：基于Reddit等社交情绪分析

### 阶段2：研究员辩论
- **看涨研究员**：提出乐观投资理由
- **看跌研究员**：提出悲观投资理由

### 阶段3：管理层决策
- **研究经理**：组织辩论并形成最终投资决策

## 📈 输出示例

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

## 🧪 独立测试

每个智能体都可以独立测试：

```bash
# 测试技术分析师
python agents/analysts/market_analyst.py

# 测试基本面分析师
python agents/analysts/fundamentals_analyst.py

# 测试看涨研究员
python agents/researchers/bull_researcher.py

# 测试数据提供模块
python data_providers/market_data.py
```

## 🔧 配置说明

### 必需配置
- `OPENAI_API_KEY`：OpenAI API密钥（必需）

### 可选配置
- `EXCHANGE_NAME`：交易所名称（默认：binance）
- `COINGECKO_API_KEY`：CoinGecko API密钥
- `CRYPTOPANIC_API_KEY`：CryptoPanic API密钥
- `TWITTER_API_KEY`：Twitter API密钥

## 📝 开发说明

### 添加新的智能体
1. 继承对应的基类（BaseAnalyst、BaseResearcher、BaseManager）
2. 实现 `process(state)` 方法
3. 添加独立测试入口
4. 在 `main.py` 中集成

### 添加新的数据源
1. 在 `data_providers/` 中创建新的数据提供类
2. 实现数据获取和预处理方法
3. 在对应的分析师中集成

## ⚠️ 注意事项

1. **API限制**：免费API有速率限制，建议合理使用
2. **数据准确性**：系统基于公开数据，投资决策需谨慎
3. **风险提示**：加密货币投资存在风险，本系统仅供参考

## 📄 许可证

MIT License

## 🤝 贡献

欢迎提交Issue和Pull Request！

## 📞 联系方式

如有问题，请提交Issue或联系开发者。 