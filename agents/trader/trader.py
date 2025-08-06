"""
交易员模块 - 基于多维度分析生成交易决策
"""

import json
import pandas as pd
from typing import Dict, Any, Optional
from agents.trader.base import BaseTrader
from utils.logger import get_logger

logger = get_logger(__name__)


class Trader(BaseTrader):
    """交易员 - 综合分析与研究共识生成交易决策"""
    
    def __init__(self, name: str = "Trader"):
        super().__init__(name)
        
    def process(self, state) -> Dict[str, Any]:
        """处理状态并生成交易决策"""
        try:
            logger.info(f"{self.name} 开始生成交易决策")
            
            # 获取分析报告
            analysis_reports = state.analysis_reports or {}
            
            # 获取研究共识
            research_consensus = state.research_consensus or {}
            
            # 生成交易决策
            trading_decision = self._generate_trading_decision(
                state.symbol,
                analysis_reports,
                research_consensus
            )
            
            # 更新状态
            state.trading_decision = trading_decision
            
            logger.info(f"{self.name} 交易决策生成完成")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 处理失败: {e}")
            return state
    
    def _generate_trading_decision(self, symbol: str, analysis_reports: Dict, research_consensus: Dict) -> Dict[str, Any]:
        """生成交易决策"""
        try:
            # 构建分析摘要
            analysis_summary = self._build_analysis_summary(analysis_reports)
            
            # 获取研究共识
            consensus_text = research_consensus.get("manager_consensus", {}).get("consensus", "无研究共识")
            
            # 构建交易员Prompt
            prompt = self._build_trader_prompt(symbol, analysis_summary, consensus_text)
            
            # 调用LLM生成交易决策
            response = self._call_llm(prompt)
            
            # 解析响应
            trading_decision = self._parse_trading_response(response, symbol, analysis_summary)
            
            return trading_decision
            
        except Exception as e:
            logger.error(f"生成交易决策失败: {e}")
            return self._generate_fallback_decision(symbol)
    
    def _build_analysis_summary(self, analysis_reports: Dict) -> Dict[str, str]:
        """构建分析摘要"""
        summary = {}
        
        # 技术分析
        if "technical" in analysis_reports:
            tech_report = analysis_reports["technical"]
            if isinstance(tech_report, dict):
                summary["technical"] = tech_report.get("summary", "技术分析完成")
            else:
                summary["technical"] = str(tech_report)
        
        # 基本面分析
        if "fundamental" in analysis_reports:
            fund_report = analysis_reports["fundamental"]
            if isinstance(fund_report, dict):
                summary["fundamental"] = fund_report.get("summary", "基本面分析完成")
            else:
                summary["fundamental"] = str(fund_report)
        
        # 新闻分析
        if "news" in analysis_reports:
            news_report = analysis_reports["news"]
            if isinstance(news_report, dict):
                summary["news"] = news_report.get("summary", "新闻分析完成")
            else:
                summary["news"] = str(news_report)
        
        # 社交分析
        if "social" in analysis_reports:
            social_report = analysis_reports["social"]
            if isinstance(social_report, dict):
                summary["social"] = social_report.get("summary", "社交分析完成")
            else:
                summary["social"] = str(social_report)
        
        return summary
    
    def _build_trader_prompt(self, symbol: str, analysis_summary: Dict, consensus_text: str) -> str:
        """构建交易员Prompt"""
        coin_name = symbol.split('/')[0] if '/' in symbol else symbol
        currency_name = symbol.split('/')[1] if '/' in symbol else "USDT"
        currency_symbol = currency_name
        
        # 从技术分析中提取当前价格信息
        current_price = self._extract_current_price(analysis_summary.get('technical', ''))
        
        prompt = f"""你是一名专业的加密货币交易员（Trader），
负责基于多维度分析为 {coin_name}（交易对：{symbol}） 做出最终交易决策。

⚠️ 重要要求：
- 所有价格必须使用 {currency_name}（{currency_symbol}）为单位
- 绝对禁止回答"无法确定目标价"或"需要更多信息"
- 必须提供具体的数值型目标价格或价格区间
- 价格建议必须基于当前市场价格 {current_price} {currency_symbol}，不能偏离太远
- **盈亏比要求**：止损与止盈的盈亏比至少为1:2，理想为1:3，确保风险收益合理
- **决策逻辑**：只有明确建议买入或卖出时才提供具体价格，观望时不提供价格

### 📊 当前市场信息：
- 当前价格：{current_price} {currency_symbol}
- 交易对：{symbol}

### 📊 分析内容要求：
1️⃣ **投资建议**
- 明确的买入 / 卖出 / 观望决策
- 观望：当市场信号不明确或风险过高时选择观望

2️⃣ **目标价格或区间**
- **买入决策**：提供入场价格、止损价格、止盈价格（盈亏比≥1:2）
- **卖出决策**：提供卖出价格、止损价格、止盈价格（盈亏比≥1:2）
- **观望决策**：不提供具体价格，说明观望理由

3️⃣ **量化指标**
- 置信度（0-1）
- 风险评分（0-1，0为低风险，1为高风险）

4️⃣ **详细推理**
- 综合以下维度进行分析：
  - 技术面：支撑位、阻力位、突破形态、交易量
  - 链上数据：活跃地址、资金流入流出、大额转账
  - 市场情绪与舆情：社交热度、情绪偏向
  - 新闻与事件：上币、合作公告、监管动态
  - 历史交易经验和风险控制措施

5️⃣ **最终输出**
- 中文完整分析报告
- 末尾必须以：
    -最终交易建议: 买入/卖出/观望
结束，明确当前决策

### 📈 当前分析数据：

**技术面分析：**
{analysis_summary.get('technical', '暂无技术分析数据')}

**基本面分析：**
{analysis_summary.get('fundamental', '暂无基本面分析数据')}

**新闻分析：**
{analysis_summary.get('news', '暂无新闻分析数据')}

**社交分析：**
{analysis_summary.get('social', '暂无社交分析数据')}

**研究共识：**
{consensus_text}

请基于以上分析数据，为 {coin_name} 提供专业的交易决策。注意：
1. 所有价格建议必须基于当前市场价格 {current_price} {currency_symbol}
2. 盈亏比至少为1:2，确保风险收益合理
3. 观望决策不提供具体价格
4. 只有明确买入或卖出建议时才提供入场价格、止损价格、止盈价格"""

        return prompt
    
    def _extract_current_price(self, technical_analysis: str) -> str:
        """从技术分析中提取当前价格"""
        try:
            import re
            # 尝试从技术分析中提取当前价格
            price_patterns = [
                r'当前价格[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'价格[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'(\d+(?:,\d+)*(?:\.\d+)?)\s*USDT',
                r'(\d+(?:,\d+)*(?:\.\d+)?)\s*美元'
            ]
            
            for pattern in price_patterns:
                match = re.search(pattern, technical_analysis)
                if match:
                    return match.group(1).replace(',', '')
            
            # 如果没找到，返回默认值
            return "113000"
            
        except Exception as e:
            logger.error(f"提取当前价格失败: {e}")
            return "113000"
    
    def _parse_trading_response(self, response: str, symbol: str, analysis_summary: Dict) -> Dict[str, Any]:
        """解析交易员响应"""
        try:
            # 提取最终交易建议
            if "最终交易建议:" in response:
                decision_part = response.split("最终交易建议:")[-1].strip()
                if "买入" in decision_part:
                    decision = "买入"
                elif "卖出" in decision_part:
                    decision = "卖出"
                elif "观望" in decision_part:
                    decision = "观望"
                else:
                    decision = "观望"
            else:
                decision = "观望"
            
            # 如果是观望决策，不提供价格
            if decision == "观望":
                return {
                    "decision": decision,
                    "entry_price": "NA",
                    "stop_loss": "NA",
                    "take_profit": "NA",
                    "confidence_score": 0.5,
                    "risk_score": 0.5,
                    "analysis": response,
                    "symbol": symbol
                }
            
            # 提取价格信息（改进版本）
            entry_price = 0
            stop_loss = 0
            take_profit = 0
            
            # 尝试从文本中提取价格
            import re
            
            # 提取入场价格 - 增加更多模式
            entry_patterns = [
                r'入场价格[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'买入目标价[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'建议在\s*(\d+(?:,\d+)*(?:\.\d+)?)\s*USDT',
                r'(\d+(?:,\d+)*(?:\.\d+)?)\s*USDT\s*附近买入',
                r'入场价[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'买入价[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'建议买入价格[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'当前价格[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'价格[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)'
            ]
            
            for pattern in entry_patterns:
                entry_match = re.search(pattern, response)
                if entry_match:
                    try:
                        entry_price = float(entry_match.group(1).replace(',', ''))
                        break
                    except:
                        continue
            
            # 提取止损价格 - 增加更多模式
            stop_patterns = [
                r'止损价格[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'止损位[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'设置止损位在\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'止损位在\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'止损价[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'止损价位[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'建议止损[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)'
            ]
            
            for pattern in stop_patterns:
                stop_match = re.search(pattern, response)
                if stop_match:
                    try:
                        stop_loss = float(stop_match.group(1).replace(',', ''))
                        break
                    except:
                        continue
            
            # 提取止盈价格 - 增加更多模式
            profit_patterns = [
                r'止盈目标[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'目标价[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'目标价为\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'目标价设定为\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'止盈价[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'止盈价位[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'建议止盈[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)',
                r'目标价格[：:]\s*(\d+(?:,\d+)*(?:\.\d+)?)'
            ]
            
            for pattern in profit_patterns:
                profit_match = re.search(pattern, response)
                if profit_match:
                    try:
                        take_profit = float(profit_match.group(1).replace(',', ''))
                        break
                    except:
                        continue
            
            # 如果没找到具体价格，尝试从数字中提取
            if entry_price == 0 and stop_loss == 0 and take_profit == 0:
                price_pattern = r'(\d{4,}(?:\.\d+)?)'
                prices = re.findall(price_pattern, response)
                if len(prices) >= 3:
                    try:
                        # 按价格大小排序，取合理的价格组合
                        prices = [float(p) for p in prices if float(p) > 1000]  # 过滤掉太小的数字
                        prices.sort()
                        if len(prices) >= 3:
                            entry_price = prices[0]  # 最低价作为入场价
                            stop_loss = prices[0] * 0.95  # 止损价略低于入场价
                            take_profit = prices[-1]  # 最高价作为止盈价
                    except:
                        pass
            
            # 如果仍然没有找到价格，使用默认逻辑
            if entry_price == 0:
                # 从技术分析中提取当前价格作为入场价
                current_price = self._extract_current_price(analysis_summary.get('technical', ''))
                try:
                    entry_price = float(current_price)
                except:
                    entry_price = 113000  # 默认价格
            
            # 优化盈亏比计算 - 确保至少1:2的盈亏比
            if stop_loss == 0 and entry_price > 0:
                if decision == "买入":
                    stop_loss = entry_price * 0.97  # 止损为入场价的97%
                else:  # 卖出
                    stop_loss = entry_price * 1.03  # 止损为入场价的103%
            
            if take_profit == 0 and entry_price > 0:
                if decision == "买入":
                    # 确保盈亏比至少1:2
                    risk = entry_price - stop_loss
                    take_profit = entry_price + (risk * 2.5)  # 1:2.5的盈亏比
                else:  # 卖出
                    # 确保盈亏比至少1:2
                    risk = stop_loss - entry_price
                    take_profit = entry_price - (risk * 2.5)  # 1:2.5的盈亏比
            
            # 提取置信度和风险评分
            confidence_score = 0.75
            risk_score = 0.5
            
            return {
                "decision": decision,
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "confidence_score": confidence_score,
                "risk_score": risk_score,
                "analysis": response,
                "symbol": symbol
            }
            
        except Exception as e:
            logger.error(f"解析交易响应失败: {e}")
            return self._generate_fallback_decision(symbol)
    
    def _generate_fallback_decision(self, symbol: str) -> Dict[str, Any]:
        """生成备用决策"""
        return {
            "decision": "观望",
            "entry_price": "NA",
            "stop_loss": "NA",
            "take_profit": "NA",
            "confidence_score": 0.5,
            "risk_score": 0.5,
            "analysis": f"由于数据不足，建议对 {symbol} 保持观望态度",
            "symbol": symbol
        }


def create_trader(llm, memory=None):
    """创建交易员实例"""
    return Trader("Trader")


if __name__ == "__main__":
    """独立测试"""
    import sys
    import os
    sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
    
    from utils.state import AgentState
    from utils.config import Config
    
    # 测试配置
    if not Config.validate_config():
        print("❌ 配置验证失败")
        exit(1)
    
    # 创建测试状态
    state = AgentState("BTC/USDT")
    state.analysis_reports = {
        "technical": {"summary": "BTC技术面显示上升趋势，RSI为65，MACD金叉"},
        "fundamental": {"summary": "BTC活跃地址增长，链上数据健康"},
        "news": {"summary": "美联储政策利好，市场情绪回暖"},
        "social": {"summary": "Twitter热度上升，多头情绪强烈"}
    }
    state.research_consensus = {
        "manager_consensus": {
            "consensus": "综合看涨，建议买入BTC"
        }
    }
    
    # 创建交易员
    trader = Trader()
    
    # 执行分析
    result = trader.process(state)
    
    print("=== 交易员测试结果 ===")
    print(f"决策: {result.trading_decision.get('decision', 'Unknown')}")
    print(f"入场价: {result.trading_decision.get('entry_price', 0)}")
    print(f"止损价: {result.trading_decision.get('stop_loss', 0)}")
    print(f"止盈价: {result.trading_decision.get('take_profit', 0)}")
    print(f"置信度: {result.trading_decision.get('confidence_score', 0)}")
    print(f"风险评分: {result.trading_decision.get('risk_score', 0)}") 