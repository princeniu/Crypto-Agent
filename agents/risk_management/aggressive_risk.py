"""
激进风险分析师
倡导高回报、高风险策略，支持交易员采取激进的操作计划
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


class AggressiveRiskManager(BaseRiskManager):
    """激进风险分析师"""
    
    def __init__(self, name: str = "Aggressive Risk Manager"):
        super().__init__(name)
    
    def process(self, state: AgentState) -> AgentState:
        """处理激进风险分析"""
        try:
            logger.info(f"{self.name} 开始分析 {state.symbol}")
            
            # 获取所有分析报告和研究共识
            analysis_reports = self.get_analysis_reports(state)
            research_consensus = self.get_research_consensus(state)
            trade_decision = self.get_trade_decision(state)
            
            if not analysis_reports:
                logger.error(f"无法获取 {state.symbol} 的分析报告")
                return state
            
            # 生成激进风险分析
            aggressive_analysis = self._generate_aggressive_analysis(state, analysis_reports, research_consensus, trade_decision)
            
            # 更新状态
            if state.risk_assessment:
                state.risk_assessment["aggressive_analysis"] = {
                    "risk_manager": self.name,
                    "analysis": aggressive_analysis,
                    "timestamp": str(pd.Timestamp.now())
                }
            else:
                state.risk_assessment = {
                    "aggressive_analysis": {
                        "risk_manager": self.name,
                        "analysis": aggressive_analysis,
                        "timestamp": str(pd.Timestamp.now())
                    }
                }
            
            logger.info(f"{self.name} 完成 {state.symbol} 激进风险分析")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 分析失败: {e}")
            return state
    
    def _generate_aggressive_analysis(self, state: AgentState, analysis_reports: Dict[str, Any], research_consensus: Dict[str, Any], trade_decision: Dict[str, Any]) -> str:
        """生成激进风险分析"""
        
        # 构建分析提示词
        prompt = self._create_aggressive_analysis_prompt(state, analysis_reports, research_consensus, trade_decision)
        
        # 调用LLM生成分析
        analysis = self.call_llm(prompt)
        
        return analysis
    
    def _create_aggressive_analysis_prompt(self, state: AgentState, analysis_reports: Dict[str, Any], research_consensus: Dict[str, Any], trade_decision: Dict[str, Any]) -> str:
        """创建激进风险分析提示词"""
        
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
你是一名专业的加密货币激进风险分析师（Risky Analyst），负责在投资辩论中倡导高回报、高风险的策略，支持交易员采取激进的操作计划。

分析目标：{state.coin_name}（交易对：{state.symbol}）

### 📊 你的任务：
1. **强调高潜在收益机会**  
   - 寻找可能带来快速上涨或爆发性收益的机会  
   - 分析短期价格波动、突破行情或事件驱动机会  
2. **主张激进策略**  
   - 即使伴随高波动或清算风险，也强调承担风险换取高收益的合理性  
3. **反驳保守与中性分析师的观点**  
   - 指出他们过于谨慎可能错失的行情机会  
   - 用数据和逻辑反驳其悲观或中性假设  
4. **数据与辩论结合**  
   - 使用以下信息强化论点：
     - 技术面：短期上升趋势、突破阻力位、成交量放大  
     - 链上数据：活跃地址增加、大额转账、资金流入  
     - 市场情绪：社交舆情、交易所热度、推特与Reddit讨论  
     - 新闻事件：上币、合作公告、机构入场或正面监管消息  
5. **动态辩论风格**  
   - 中文对话式表达，像在实时辩论中说服对方  
   - 直接回应保守与中性分析师提出的担忧，逐条反击  

### 可用信息：

## 市场技术分析报告
{technical_analysis}

## 社交情绪分析
{social_analysis}

## 最新加密新闻与事件
{news_analysis}

## 链上与基本面报告
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
- 中文自然辩论风格表达，不使用机械清单式输出  
- 明确提出高风险高回报的投资理由  
- 针对对手观点逐条反驳  
- 突出激进策略的潜在收益与市场机会
- 强调在当前市场环境下激进策略的优势
"""

        return prompt


def create_aggressive_risk_manager(llm=None, memory=None):
    """创建激进风险管理实例"""
    return AggressiveRiskManager("Aggressive Risk Manager")


if __name__ == "__main__":
    # 独立测试
    print("=== 激进风险分析师独立测试 ===")
    
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
    risk_manager = AggressiveRiskManager()
    
    # 执行分析
    result_state = risk_manager.process(state)
    
    # 输出结果
    print(f"\n分析完成！")
    print(f"币种: {result_state.symbol}")
    
    risk_assessment = result_state.risk_assessment
    if risk_assessment:
        aggressive_analysis = risk_assessment.get("aggressive_analysis", {})
        print(f"\n激进风险分析:")
        print(f"风险管理器: {aggressive_analysis.get('risk_manager', 'Unknown')}")
        print(f"分析内容: {aggressive_analysis.get('analysis', 'No analysis')[:200]}...")
    else:
        print("未生成激进风险分析")
    
    print("\n测试完成！") 