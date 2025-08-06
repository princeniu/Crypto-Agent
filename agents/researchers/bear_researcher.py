"""
看跌研究员
基于分析报告生成看跌观点和风险提示
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


class BearResearcher(BaseResearcher):
    """看跌研究员"""
    
    def __init__(self, name: str = "Bear Researcher"):
        super().__init__(name)
    
    def process(self, state: AgentState) -> AgentState:
        """处理看跌分析"""
        try:
            logger.info(f"{self.name} 开始分析 {state.symbol}")
            
            # 获取所有分析报告
            analysis_reports = self.get_analysis_reports(state)
            
            if not analysis_reports:
                logger.error(f"无法获取 {state.symbol} 的分析报告")
                return state
            
            # 生成看跌观点
            bear_analysis = self._generate_bear_analysis(state, analysis_reports)
            
            # 更新状态
            if state.research_consensus:
                state.research_consensus["bear_analysis"] = {
                    "researcher": self.name,
                    "analysis": bear_analysis,
                    "timestamp": str(pd.Timestamp.now())
                }
            else:
                state.research_consensus = {
                    "bear_analysis": {
                        "researcher": self.name,
                        "analysis": bear_analysis,
                        "timestamp": str(pd.Timestamp.now())
                    }
                }
            
            logger.info(f"{self.name} 完成 {state.symbol} 看跌分析")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 分析失败: {e}")
            return state
    
    def _generate_bear_analysis(self, state: AgentState, analysis_reports: Dict[str, Any]) -> str:
        """生成看跌分析"""
        
        # 构建分析提示词
        prompt = self._create_bear_analysis_prompt(state, analysis_reports)
        
        # 调用LLM生成分析
        analysis = self.call_llm(prompt)
        
        return analysis
    
    def _create_bear_analysis_prompt(self, state: AgentState, analysis_reports: Dict[str, Any]) -> str:
        """创建看跌分析提示词"""
        
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
你是一名专业的加密货币看跌分析师（Bear Researcher），负责为 {state.coin_name}（交易对：{state.symbol}） 的投资识别潜在风险和看跌因素。

⚠️ 注意：所有价格或估值请使用 {state.currency_name}（{state.currency_symbol}）作为单位。

你的任务是基于真实数据和分析报告，提出客观的看跌观点，识别潜在风险，并给出谨慎的投资建议。

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

1️⃣ **市场风险因素**  
- 宏观经济环境的不利影响（加息、通胀、地缘政治）  
- 监管政策变化对加密货币的潜在负面影响  
- 市场流动性不足和波动性增加的风险

2️⃣ **项目特定风险**  
- 代币经济模型的潜在问题（通胀、集中度）  
- 技术实现和安全性风险  
- 竞争加剧和市场份额流失的风险

3️⃣ **负面指标**  
- 链上数据：交易量下降、资金流出、活跃度降低  
- 市场指标：技术面空头信号、跌破关键支撑位  
- 新闻与舆情：近期利空消息、投资者情绪消极

4️⃣ **反驳看涨论点**  
- 指出看涨论点的潜在漏洞和过度乐观之处
- 用真实数据和逻辑证明下跌的可能性

5️⃣ **风险控制建议**  
- 以自然中文表达你的看跌观点  
- 提供具体的风险控制措施和投资建议

请基于以上信息，提出客观的看跌论点，并呈现动态辩论风格。  
所有回答必须为中文，适合直接写入投资辩论历史。

要求：
- 所有分析必须基于提供的真实数据
- 论点要客观、专业、有说服力
- 报告长度不少于800字
- 重点关注风险因素和下行可能性
"""

        return prompt


def create_bear_researcher(llm=None, memory=None):
    """创建看跌研究员实例"""
    return BearResearcher("Bear Researcher")


if __name__ == "__main__":
    # 独立测试
    print("=== 看跌研究员独立测试 ===")
    
    # 创建状态
    state = AgentState("BTC/USDT")
    
    # 模拟分析报告
    state.update_analysis_report("technical", {
        "analyst": "Market Analyst",
        "analysis": "BTC技术面显示空头趋势，RSI为35，MACD死叉，布林带显示价格在下降通道中。"
    })
    
    state.update_analysis_report("fundamental", {
        "analyst": "Fundamentals Analyst", 
        "analysis": "BTC基本面存在担忧，机构资金流出，监管压力增加，市场信心不足。"
    })
    
    state.update_analysis_report("news", {
        "analyst": "News Analyst",
        "analysis": "近期新闻情绪负面，监管收紧，机构投资减少，市场恐慌情绪上升。"
    })
    
    state.update_analysis_report("social", {
        "analyst": "Social Media Analyst",
        "analysis": "社交媒体情绪消极，Reddit讨论热度下降，用户情绪偏向悲观。"
    })
    
    # 创建研究员
    researcher = BearResearcher()
    
    # 执行分析
    result_state = researcher.process(state)
    
    # 输出结果
    print(f"\n分析完成！")
    print(f"币种: {result_state.symbol}")
    
    research_consensus = result_state.research_consensus
    if research_consensus:
        bear_analysis = research_consensus.get("bear_analysis", {})
        print(f"\n看跌分析:")
        print(f"研究员: {bear_analysis.get('researcher', 'Unknown')}")
        print(f"分析内容: {bear_analysis.get('analysis', 'No analysis')[:200]}...")
    else:
        print("未生成看跌分析")
    
    print("\n测试完成！") 