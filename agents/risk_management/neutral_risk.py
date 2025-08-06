"""
中性风险分析师
提供平衡视角，权衡潜在收益与风险，提出中性、可持续的操作方案
"""

import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from typing import Dict, Any
from agents.risk_management.base import BaseRiskManager
from utils.state import AgentState
from utils.logger import get_logger

logger = get_logger(__name__)


class NeutralRiskManager(BaseRiskManager):
    """中性风险分析师"""
    
    def __init__(self, name: str = "Neutral Risk Manager"):
        super().__init__(name)
    
    def process(self, state: AgentState) -> AgentState:
        """处理中性风险分析"""
        try:
            logger.info(f"{self.name} 开始分析 {state.symbol}")
            
            # 获取所有分析报告和研究共识
            analysis_reports = self.get_analysis_reports(state)
            research_consensus = self.get_research_consensus(state)
            trade_decision = self.get_trade_decision(state)
            
            if not analysis_reports:
                logger.error(f"无法获取 {state.symbol} 的分析报告")
                return state
            
            # 生成中性风险分析
            neutral_analysis = self._generate_neutral_analysis(state, analysis_reports, research_consensus, trade_decision)
            
            # 更新状态
            if state.risk_assessment:
                state.risk_assessment["neutral_analysis"] = {
                    "risk_manager": self.name,
                    "analysis": neutral_analysis,
                    "timestamp": str(pd.Timestamp.now())
                }
            else:
                state.risk_assessment = {
                    "neutral_analysis": {
                        "risk_manager": self.name,
                        "analysis": neutral_analysis,
                        "timestamp": str(pd.Timestamp.now())
                    }
                }
            
            logger.info(f"{self.name} 完成 {state.symbol} 中性风险分析")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 分析失败: {e}")
            return state
    
    def _generate_neutral_analysis(self, state: AgentState, analysis_reports: Dict[str, Any], research_consensus: Dict[str, Any], trade_decision: Dict[str, Any]) -> str:
        """生成中性风险分析"""
        
        # 构建分析提示词
        prompt = self._create_neutral_analysis_prompt(state, analysis_reports, research_consensus, trade_decision)
        
        # 调用LLM生成分析
        analysis = self.call_llm(prompt)
        
        return analysis
    
    def _create_neutral_analysis_prompt(self, state: AgentState, analysis_reports: Dict[str, Any], research_consensus: Dict[str, Any], trade_decision: Dict[str, Any]) -> str:
        """创建中性风险分析提示词"""
        
        # 提取分析报告
        technical_report = analysis_reports.get("technical", {})
        fundamental_report = analysis_reports.get("fundamental", {})
        news_report = analysis_reports.get("news", {})
        social_report = analysis_reports.get("social", {})
        
        # 提取研究共识
        bull_analysis = research_consensus.get("bull_analysis", {})
        bear_analysis = research_consensus.get("bear_analysis", {})
        manager_consensus = research_consensus.get("manager_consensus", {})
        
        # 提取交易决策
        trader_decision = trade_decision.get("decision", "无交易决策")
        
        # 提取分析内容
        technical_analysis = technical_report.get("analysis", "无技术分析数据")
        fundamental_analysis = fundamental_report.get("analysis", "无基本面分析数据")
        news_analysis = news_report.get("analysis", "无新闻分析数据")
        social_analysis = social_report.get("analysis", "无社交分析数据")
        
        bull_analysis_text = bull_analysis.get("analysis", "无看涨分析数据")
        bear_analysis_text = bear_analysis.get("analysis", "无看跌分析数据")
        manager_consensus_text = manager_consensus.get("consensus", "无研究经理共识")
        
        prompt = f"""
你是一名专业的加密货币中性风险分析师（Neutral Analyst），你的角色是提供平衡视角，权衡 {state.coin_name}（交易对：{state.symbol}） 的潜在收益与风险。

### 📊 你的任务：
1️⃣ **平衡分析**  
- 同时评估短期上涨潜力与下行风险  
- 考虑市场波动性、链上数据变化和潜在极端事件（清算、黑客攻击、监管利空）  
- 权衡激进与保守策略的利弊，提出中性、可持续的操作方案  

2️⃣ **批判双方观点**  
- 指出激进分析师过于乐观、忽视风险的部分  
- 指出保守分析师过于谨慎、可能错失市场机会的地方  

3️⃣ **提出中性操作建议**  
- 建议适度仓位、分批建仓或采取对冲/保护性措施  
- 强调在高波动加密市场中稳健收益的重要性  
- 建议利用止损、止盈和多币种分散策略平衡风险与收益  

4️⃣ **动态辩论风格**  
- 中文自然口语表达，仿佛在现场辩论  
- 逐条回应激进与保守分析师的最新发言  
- 重点说明为什么中庸策略可以提供相对可靠的长期回报  

### 可用信息：

## 市场技术分析报告
{technical_analysis}

## 社交舆情与情绪分析
{social_analysis}

## 最新加密新闻与事件
{news_analysis}

## 链上与基本面分析报告
{fundamental_analysis}

## 看涨研究员观点
{bull_analysis_text}

## 看跌研究员观点
{bear_analysis_text}

## 研究经理共识
{manager_consensus_text}

## 交易员初步投资计划
{trader_decision}

### 💡 输出要求：
- 中文自然辩论风格，直接回应双方观点  
- 提供明确的中性操作建议（如适度仓位、分批建仓、止损保护）  
- 强调风险收益平衡与可持续性
- 突出中庸策略在波动市场中的优势
"""

        return prompt


def create_neutral_risk_manager(llm=None, memory=None):
    """创建中性风险管理实例"""
    return NeutralRiskManager("Neutral Risk Manager")


if __name__ == "__main__":
    # 独立测试
    print("=== 中性风险分析师独立测试 ===")
    
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
    
    # 模拟研究共识
    state.research_consensus = {
        "bull_analysis": {
            "researcher": "Bull Researcher",
            "analysis": "基于技术面和基本面分析，BTC具有强劲的上涨潜力，建议买入。"
        },
        "bear_analysis": {
            "researcher": "Bear Researcher", 
            "analysis": "虽然基本面良好，但技术面存在回调风险，建议谨慎持有。"
        },
        "manager_consensus": {
            "manager": "Research Manager",
            "consensus": "综合各方观点，建议适度买入，关注风险控制。"
        }
    }
    
    # 模拟交易决策
    state.trade_decision = {
        "decision": "基于分析结果，建议买入BTC，目标价格120000 USDT。"
    }
    
    # 创建风险管理器
    risk_manager = NeutralRiskManager()
    
    # 执行分析
    result_state = risk_manager.process(state)
    
    # 输出结果
    print(f"\n分析完成！")
    print(f"币种: {result_state.symbol}")
    
    risk_assessment = result_state.risk_assessment
    if risk_assessment:
        neutral_analysis = risk_assessment.get("neutral_analysis", {})
        print(f"\n中性风险分析:")
        print(f"风险管理器: {neutral_analysis.get('risk_manager', 'Unknown')}")
        print(f"分析内容: {neutral_analysis.get('analysis', 'No analysis')[:200]}...")
    else:
        print("未生成中性风险分析")
    
    print("\n测试完成！") 