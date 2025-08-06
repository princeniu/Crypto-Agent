"""
看涨研究员
基于分析报告生成看涨观点和投资理由
"""

import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from typing import Dict, Any
from agents.researchers.base import BaseResearcher
from utils.state import AgentState
from utils.logger import get_logger

logger = get_logger(__name__)


class BullResearcher(BaseResearcher):
    """看涨研究员"""
    
    def __init__(self, name: str = "Bull Researcher"):
        super().__init__(name)
    
    def process(self, state: AgentState) -> AgentState:
        """处理看涨分析"""
        try:
            logger.info(f"{self.name} 开始分析 {state.symbol}")
            
            # 获取所有分析报告
            analysis_reports = self.get_analysis_reports(state)
            
            if not analysis_reports:
                logger.error(f"无法获取 {state.symbol} 的分析报告")
                return state
            
            # 生成看涨观点
            bull_analysis = self._generate_bull_analysis(state, analysis_reports)
            
            # 更新状态
            state.research_consensus = {
                "bull_analysis": {
                    "researcher": self.name,
                    "analysis": bull_analysis,
                    "timestamp": str(pd.Timestamp.now())
                }
            }
            
            logger.info(f"{self.name} 完成 {state.symbol} 看涨分析")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 分析失败: {e}")
            return state
    
    def _generate_bull_analysis(self, state: AgentState, analysis_reports: Dict[str, Any]) -> str:
        """生成看涨分析"""
        
        # 构建分析提示词
        prompt = self._create_bull_analysis_prompt(state, analysis_reports)
        
        # 调用LLM生成分析
        analysis = self.call_llm(prompt)
        
        return analysis
    
    def _create_bull_analysis_prompt(self, state: AgentState, analysis_reports: Dict[str, Any]) -> str:
        """创建看涨分析提示词"""
        
        technical_report = analysis_reports.get("technical", {})
        fundamental_report = analysis_reports.get("fundamental", {})
        news_report = analysis_reports.get("news", {})
        social_report = analysis_reports.get("social", {})
        
        # 提取分析内容
        technical_analysis = technical_report.get("analysis", "无技术分析数据")
        fundamental_analysis = fundamental_report.get("analysis", "无基本面分析数据")
        news_analysis = news_report.get("analysis", "无新闻分析数据")
        social_analysis = social_report.get("analysis", "无社交分析数据")
        
        prompt = f"""
你是一名专业的加密货币看涨分析师（Bull Researcher），负责为 {state.coin_name}（交易对：{state.symbol}） 的投资构建强有力的看涨论点。

⚠️ 注意：所有价格或估值请使用 {state.currency_name}（{state.currency_symbol}）作为单位。

你的任务是基于真实数据和分析报告，提出令人信服的看涨观点，展示该加密货币的上涨潜力，并有效反驳看跌论点。

📊 可用分析报告：

## 技术分析报告
{technical_analysis}

## 基本面分析报告
{fundamental_analysis}

## 新闻分析报告
{news_analysis}

## 社交情绪分析报告
{social_analysis}

请重点关注以下方面：

1️⃣ **增长潜力**  
- 行业或生态发展的积极趋势（如DeFi、NFT、L2或跨链生态）  
- 代币应用场景、用户增长、活跃地址数提升  
- 潜在利好事件（上币、机构入场、链上升级等）

2️⃣ **竞争优势**  
- 代币经济模型优越（稀缺性、销毁机制、合理的通胀率）  
- 项目在行业的独特地位或技术领先性  
- 社区活跃度高、开发者生态强大

3️⃣ **积极指标**  
- 链上数据：交易量增长、资金流入、活跃度上升  
- 市场指标：技术面多头信号、突破关键阻力位  
- 新闻与舆情：近期利好消息、投资者情绪积极

4️⃣ **反驳看跌论点**  
- 指出可能的看跌担忧并给出积极回应
- 用真实数据和逻辑证明上涨的合理性与可持续性

5️⃣ **参与动态辩论**  
- 以自然中文表达你的看涨论点  
- 增强团队对看涨立场的信心

请基于以上信息，提出充分的看涨论点，并呈现动态辩论风格。  
所有回答必须为中文，适合直接写入投资辩论历史。

要求：
- 所有分析必须基于提供的真实数据
- 论点要具体、专业、有说服力
- 报告长度不少于800字
- 重点关注上涨潜力和积极因素
"""

        return prompt


def create_bull_researcher(llm=None, memory=None):
    """创建看涨研究员实例"""
    return BullResearcher("Bull Researcher")


if __name__ == "__main__":
    # 独立测试
    print("=== 看涨研究员独立测试 ===")
    
    # 创建状态
    state = AgentState("BTC/USDT")
    
    # 模拟分析报告
    state.update_analysis_report("technical", {
        "analyst": "Market Analyst",
        "analysis": "BTC技术面显示多头趋势，RSI为65，MACD金叉，布林带显示价格在上升通道中。"
    })
    
    state.update_analysis_report("fundamental", {
        "analyst": "Fundamentals Analyst", 
        "analysis": "BTC基本面强劲，市值排名第一，机构采用率持续增长，长期价值看好。"
    })
    
    state.update_analysis_report("news", {
        "analyst": "News Analyst",
        "analysis": "近期新闻情绪正面，机构投资增加，监管环境改善，市场信心回升。"
    })
    
    state.update_analysis_report("social", {
        "analyst": "Social Media Analyst",
        "analysis": "社交媒体情绪积极，Reddit讨论热度高，用户情绪偏向乐观。"
    })
    
    # 创建研究员
    researcher = BullResearcher()
    
    # 执行分析
    result_state = researcher.process(state)
    
    # 输出结果
    print(f"\n分析完成！")
    print(f"币种: {result_state.symbol}")
    
    research_consensus = result_state.research_consensus
    if research_consensus:
        bull_analysis = research_consensus.get("bull_analysis", {})
        print(f"\n看涨分析:")
        print(f"研究员: {bull_analysis.get('researcher', 'Unknown')}")
        print(f"分析内容: {bull_analysis.get('analysis', 'No analysis')[:200]}...")
    else:
        print("未生成看涨分析")
    
    print("\n测试完成！") 