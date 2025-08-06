"""
研究经理
组织研究员辩论并形成研究共识
"""

import sys
import os
import pandas as pd
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from typing import Dict, Any
from agents.managers.base import BaseManager
from utils.state import AgentState
from utils.logger import get_logger

logger = get_logger(__name__)


class ResearchManager(BaseManager):
    """研究经理"""
    
    def __init__(self, name: str = "Research Manager"):
        super().__init__(name)
    
    def process(self, state: AgentState) -> AgentState:
        """处理研究共识"""
        try:
            logger.info(f"{self.name} 开始处理 {state.symbol} 研究共识")
            
            # 获取所有分析报告和研究共识
            analysis_reports = self.get_analysis_reports(state)
            research_consensus = self.get_research_consensus(state)
            
            if not analysis_reports:
                logger.error(f"无法获取 {state.symbol} 的分析报告")
                return state
            
            # 生成研究共识
            consensus_result = self._generate_research_consensus(state, analysis_reports, research_consensus)
            
            # 更新状态
            if state.research_consensus:
                state.research_consensus["manager_consensus"] = {
                    "manager": self.name,
                    "consensus": consensus_result,
                    "timestamp": str(pd.Timestamp.now())
                }
            else:
                state.research_consensus = {
                    "manager_consensus": {
                        "manager": self.name,
                        "consensus": consensus_result,
                        "timestamp": str(pd.Timestamp.now())
                    }
                }
            
            logger.info(f"{self.name} 完成 {state.symbol} 研究共识")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 处理失败: {e}")
            return state
    
    def _generate_research_consensus(self, state: AgentState, analysis_reports: Dict[str, Any], research_consensus: Dict[str, Any]) -> str:
        """生成研究共识"""
        
        # 构建分析提示词
        prompt = self._create_research_consensus_prompt(state, analysis_reports, research_consensus)
        
        # 调用LLM生成共识
        consensus = self.call_llm(prompt)
        
        return consensus
    
    def _create_research_consensus_prompt(self, state: AgentState, analysis_reports: Dict[str, Any], research_consensus: Dict[str, Any]) -> str:
        """创建研究共识提示词"""
        
        # 提取分析报告
        technical_report = analysis_reports.get("technical", {})
        fundamental_report = analysis_reports.get("fundamental", {})
        news_report = analysis_reports.get("news", {})
        social_report = analysis_reports.get("social", {})
        
        # 提取研究共识
        bull_analysis = research_consensus.get("bull_analysis", {}) if research_consensus else {}
        bear_analysis = research_consensus.get("bear_analysis", {}) if research_consensus else {}
        
        technical_analysis = technical_report.get("analysis", "无技术分析数据")
        fundamental_analysis = fundamental_report.get("analysis", "无基本面分析数据")
        news_analysis = news_report.get("analysis", "无新闻分析数据")
        social_analysis = social_report.get("analysis", "无社交分析数据")
        
        bull_analysis_text = bull_analysis.get("analysis", "无看涨分析数据")
        bear_analysis_text = bear_analysis.get("analysis", "无看跌分析数据")
        
        prompt = f"""
你是一位专业的加密货币投资组合经理和辩论主持人。

分析目标：{state.coin_name}（交易对：{state.symbol}）

📊 你的职责：
1. 总结看多与看空研究员的核心论点，强调最有说服力的证据或逻辑。
2. 结合多维度报告形成综合分析：
   - 技术分析（市场趋势、支撑阻力）
   - 社交舆情与情绪分析
   - 新闻与重大事件对价格的潜在影响
   - 基本面或链上数据分析（市值、活跃地址、交易量、资金流入流出）
3. 做出明确投资建议：**买入 / 卖出 / 持有**  
   - 避免因为两方观点都有道理就机械选择"持有"
   - 必须基于最有力的论点做出承诺

📋 可用分析报告：

## 技术分析报告
{technical_analysis}

## 基本面分析报告
{fundamental_analysis}

## 新闻分析报告
{news_analysis}

## 社交情绪分析报告
{social_analysis}

## 看涨研究员观点
{bull_analysis_text}

## 看跌研究员观点
{bear_analysis_text}

💡 投资计划必须包括：
1. **投资建议**：基于最有力论点的明确立场  
2. **理由说明**：为什么得出这个结论  
3. **战略行动**：
   - 建仓或减仓策略  
   - 风险控制措施（止损、止盈、仓位比例）  
4. **目标价格分析**：
   - 提供目标价格区间（以{state.currency_name}{state.currency_symbol}计价）  
   - 基于以下维度：
     - 链上与基本面数据（市值、活跃度）
     - 新闻与事件驱动
     - 社交情绪与市场热度
     - 技术支撑与阻力位
   - 提供三种情景：保守 / 基准 / 乐观  
   - 给出价格目标对应的时间范围（1周、1个月、3个月）  
5. **过往经验反思**：
   - 考虑你在类似市场条件下的历史失误  
   - 结合历史反思优化当前决策

📈 输出要求：
- 输出完整中文分析报告  
- 明确给出投资建议与可执行计划  
- 提供具体价格区间与时间周期  
- 不允许回答"无法确定"或"需要更多信息"  
- 自然表达，如同在和交易团队口头汇报

要求：
- 所有分析必须基于提供的真实数据
- 投资建议必须使用中文（买入/持有/卖出）
- 报告长度不少于1000字
- 分析要具体、专业、有说服力
- 重点关注最有力的论点和证据
"""

        return prompt


def create_research_manager(llm=None, memory=None):
    """创建研究经理实例"""
    return ResearchManager("Research Manager")


if __name__ == "__main__":
    # 独立测试
    print("=== 研究经理独立测试 ===")
    
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
        }
    }
    
    # 创建研究经理
    manager = ResearchManager()
    
    # 执行分析
    result_state = manager.process(state)
    
    # 输出结果
    print(f"\n分析完成！")
    print(f"币种: {result_state.symbol}")
    
    research_consensus = result_state.research_consensus
    if research_consensus:
        manager_consensus = research_consensus.get("manager_consensus", {})
        print(f"\n研究经理共识:")
        print(f"经理: {manager_consensus.get('manager', 'Unknown')}")
        print(f"共识内容: {manager_consensus.get('consensus', 'No consensus')[:200]}...")
    else:
        print("未生成研究共识")
    
    print("\n测试完成！") 