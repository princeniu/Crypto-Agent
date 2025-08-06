"""
技术分析师
基于K线数据和技术指标进行技术分析
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from typing import Dict, Any
from agents.analysts.base import BaseAnalyst
from utils.state import AgentState
from utils.logger import get_logger
from data_providers.market_data import MarketDataProvider

logger = get_logger(__name__)


class MarketAnalyst(BaseAnalyst):
    """技术分析师"""
    
    def __init__(self, name: str = "Market Analyst"):
        super().__init__(name)
        self.market_provider = MarketDataProvider()
    
    def process(self, state: AgentState) -> AgentState:
        """处理技术分析"""
        try:
            logger.info(f"{self.name} 开始分析 {state.symbol}")
            
            # 获取市场数据
            market_data = self.market_provider.get_market_data(state.symbol)
            
            if not market_data:
                logger.error(f"无法获取 {state.symbol} 的市场数据")
                return state
            
            # 生成技术分析报告
            analysis_result = self._generate_technical_analysis(state, market_data)
            
            # 更新状态
            self.update_state_with_analysis(state, "technical", analysis_result)
            
            logger.info(f"{self.name} 完成 {state.symbol} 技术分析")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 分析失败: {e}")
            return state
    
    def _generate_technical_analysis(self, state: AgentState, market_data: Dict[str, Any]) -> str:
        """生成技术分析报告"""
        
        # 构建分析提示词
        prompt = self._create_technical_analysis_prompt(state, market_data)
        
        # 调用LLM生成分析
        analysis = self.call_llm(prompt)
        
        return analysis
    
    def _create_technical_analysis_prompt(self, state: AgentState, market_data: Dict[str, Any]) -> str:
        """创建技术分析提示词"""
        
        current_price = market_data.get('current_price', 0)
        price_change = market_data.get('price_change_24h', 0)
        trend = market_data.get('trend', 'neutral')
        volume = market_data.get('volume_24h', 0)
        
        technical_indicators = market_data.get('technical_indicators', {})
        rsi = technical_indicators.get('rsi', 50)
        macd_data = technical_indicators.get('macd', {})
        bb_data = technical_indicators.get('bollinger_bands', {})
        
        support_resistance = market_data.get('support_resistance', {})
        resistance_levels = support_resistance.get('resistance_levels', [])
        support_levels = support_resistance.get('support_levels', [])
        
        prompt = f"""
你是一位专业的加密货币技术分析师。

分析目标：{state.coin_name}（交易对：{state.symbol}）

📊 市场数据：
- 当前价格：{current_price:.2f} {state.currency_symbol}
- 24小时涨跌幅：{price_change:.2f}%
- 趋势方向：{trend}
- 24小时成交量：{volume:.2f}

📈 技术指标：
- RSI：{rsi:.2f}
- MACD：{macd_data}
- 布林带：{bb_data}

📉 支撑阻力位：
- 阻力位：{resistance_levels}
- 支撑位：{support_levels}

请基于以上真实数据进行技术分析，生成完整的中文技术分析报告，包括：

## 📊 币种基本信息
- 币种名称：{state.coin_name}
- 交易对：{state.symbol}
- 当前价格、24小时涨跌幅、交易量

## 📈 技术指标分析
- MACD、RSI、布林带分析
- 指标数值与含义解释

## 📉 价格趋势分析
- 短期/中期趋势方向
- 关键支撑位与阻力位

## 🔹 市场情绪分析
- 基于技术指标的市场情绪判断

## 💭 投资建议
- 买入/持有/卖出建议（中文表达）
- 简要说明风险或条件

要求：
- 所有分析必须基于提供的真实数据
- 投资建议必须使用中文（买入/持有/卖出）
- 报告长度不少于600字
- 分析要具体、专业、有说服力
"""

        return prompt


def create_market_analyst(llm=None, memory=None):
    """创建技术分析师实例"""
    return MarketAnalyst("Market Analyst")


if __name__ == "__main__":
    # 独立测试
    print("=== 技术分析师独立测试 ===")
    
    # 创建状态
    state = AgentState("BTC/USDT")
    
    # 创建分析师
    analyst = MarketAnalyst()
    
    # 执行分析
    result_state = analyst.process(state)
    
    # 输出结果
    print(f"\n分析完成！")
    print(f"币种: {result_state.symbol}")
    
    technical_report = result_state.analysis_reports.get("technical")
    if technical_report:
        print(f"\n技术分析报告:")
        print(f"分析师: {technical_report.get('analyst', 'Unknown')}")
        print(f"分析内容: {technical_report.get('analysis', 'No analysis')[:200]}...")
    else:
        print("未生成技术分析报告")
    
    print("\n测试完成！") 