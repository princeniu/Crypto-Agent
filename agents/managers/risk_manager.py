"""
风险经理模块 - 综合风险评估并做出最终决策
"""

import json
import pandas as pd
from typing import Dict, Any, List
from agents.managers.base import BaseManager
from agents.risk_management.aggressive_risk import AggressiveRiskManager
from agents.risk_management.neutral_risk import NeutralRiskManager
from agents.risk_management.conservative_risk import ConservativeRiskManager
from utils.logger import get_logger

logger = get_logger(__name__)


class RiskManager(BaseManager):
    """风险经理 - 综合风险评估并做出最终决策"""
    
    def __init__(self, name: str = "Risk Manager"):
        super().__init__(name)
        
        # 初始化风险评估员
        self.risk_assessors = [
            AggressiveRiskManager("Aggressive Risk Assessor"),
            NeutralRiskManager("Neutral Risk Assessor"),
            ConservativeRiskManager("Conservative Risk Assessor")
        ]
    
    def process(self, state) -> Dict[str, Any]:
        """处理状态并生成风险评估"""
        try:
            logger.info(f"{self.name} 开始风险评估")
            
            # 获取交易决策
            trading_decision = state.trading_decision or {}
            
            # 获取分析报告
            analysis_reports = state.analysis_reports or {}
            
            # 执行风险评估
            risk_assessment = self._conduct_risk_assessment(
                state.symbol,
                trading_decision,
                analysis_reports
            )
            
            # 生成最终风险决策
            final_risk_decision = self._generate_final_risk_decision(
                state.symbol,
                risk_assessment,
                trading_decision
            )
            
            # 更新状态
            state.risk_assessment = risk_assessment
            state.final_risk_decision = final_risk_decision
            
            logger.info(f"{self.name} 风险评估完成")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 处理失败: {e}")
            return state
    
    def _conduct_risk_assessment(self, symbol: str, trading_decision: Dict, analysis_reports: Dict) -> Dict[str, Any]:
        """执行风险评估"""
        try:
            risk_results = {}
            
            # 让每个风险评估员进行评估
            for assessor in self.risk_assessors:
                try:
                    logger.info(f"执行 {assessor.name} 风险评估")
                    
                    # 创建临时状态用于风险评估
                    coin_name = symbol.split('/')[0] if '/' in symbol else symbol
                    temp_state = type('TempState', (), {
                        'symbol': symbol,
                        'coin_name': coin_name,
                        'trading_decision': trading_decision,
                        'trade_decision': trading_decision,  # 添加别名
                        'analysis_reports': analysis_reports,
                        'research_consensus': {},
                        'risk_assessment': {},
                        'get_all_analysis_reports': lambda self: analysis_reports,
                        'get_research_consensus': lambda self: {},
                        'get_trade_decision': lambda self: trading_decision
                    })()
                    
                    # 执行风险评估
                    result = assessor.process(temp_state)
                    
                    # 提取风险评估结果
                    if hasattr(result, 'risk_assessment'):
                        risk_results[assessor.name] = result.risk_assessment
                    else:
                        risk_results[assessor.name] = {
                            "risk_level": "medium",
                            "risk_score": 0.5,
                            "recommendation": "建议观望",
                            "analysis": "风险评估完成"
                        }
                        
                except Exception as e:
                    logger.error(f"{assessor.name} 风险评估失败: {e}")
                    risk_results[assessor.name] = {
                        "risk_level": "medium",
                        "risk_score": 0.5,
                        "recommendation": "建议观望",
                        "analysis": f"风险评估失败: {str(e)}"
                    }
            
            return risk_results
            
        except Exception as e:
            logger.error(f"执行风险评估失败: {e}")
            return self._generate_fallback_risk_assessment(symbol)
    
    def _generate_final_risk_decision(self, symbol: str, risk_assessment: Dict, trading_decision: Dict) -> Dict[str, Any]:
        """生成最终风险决策"""
        try:
            # 构建风险经理Prompt
            prompt = self._build_risk_manager_prompt(symbol, risk_assessment, trading_decision)
            
            # 调用LLM生成最终决策
            response = self.call_llm(prompt)
            
            # 解析响应
            final_decision = self._parse_risk_response(response, symbol)
            
            return final_decision
            
        except Exception as e:
            logger.error(f"生成最终风险决策失败: {e}")
            return self._generate_fallback_risk_decision(symbol)
    
    def _build_risk_manager_prompt(self, symbol: str, risk_assessment: Dict, trading_decision: Dict) -> str:
        """构建风险经理Prompt"""
        coin_name = symbol.split('/')[0] if '/' in symbol else symbol
        
        # 构建风险评估摘要
        risk_summary = self._build_risk_summary(risk_assessment)
        
        # 构建交易决策摘要
        trading_summary = self._build_trading_summary(trading_decision)
        
        prompt = f"""你是一位专业的加密货币风险管理委员会主席和风险辩论主持人。  
⚠️ 你的任务是综合三位风险分析师（激进 / 中性 / 保守）的观点，评估当前加密货币交易策略风险，并输出最终决策（买入 / 卖出 / 持有）。

分析目标：{coin_name}（交易对：{symbol}）

### 📊 你的职责：
1. **总结辩论关键点**：
   - 汇总三位风险分析师的核心观点
   - 重点识别潜在风险来源，包括：
     - 市场波动性（短期价格剧烈波动风险）
     - 链上安全风险（黑客攻击、巨鲸转账、合约漏洞）
     - 交易所与流动性风险（下架、提现限制、流动性不足）
     - 政策与宏观风险（监管政策、全球经济事件）
2. **给出明确的风险决策**：
   - 买入 / 卖出 / 持有（三选一）
   - 必须基于风险评估结果和交易员决策综合考虑
   - 如果交易员建议买入但风险较高，可以建议持有或降低仓位
   - 如果交易员建议卖出但风险较低，可以建议持有或观望
3. **优化交易员计划**：
   - 在原交易员计划的基础上，提出风险控制和仓位调整建议
   - 明确止损价位、止盈目标和仓位百分比
   - 确保风险决策与交易决策的逻辑一致性
4. **结合历史经验改进决策**：
   - 使用过往风险管理失误的经验来避免重复错误
   - 强调如何在波动市场中保护资金安全

### 💡 输出要求：
- 中文详细分析报告
- 必须包含：
  1. 明确最终风险决策（买入 / 卖出 / 持有）
  2. 支撑决策的主要理由
  3. 风险控制策略（止损、止盈、仓位比例）
  4. 风险来源清单（市场、链上、交易所、政策）
- 建议附上短期风险预警（未来1-7天的主要风险）
- 自然表达，如同给交易团队口头汇报
- 不允许输出模糊建议或"无法确定"
- 确保风险决策与交易员决策的逻辑协调

### 📈 当前数据：

**交易员决策：**
{trading_summary}

**风险评估结果：**
{risk_summary}

请基于以上数据，为 {coin_name} 提供最终的风险管理决策。注意：你的决策应该与交易员决策保持逻辑一致性，如果存在冲突，请说明理由并提供协调方案。"""

        return prompt
    
    def _build_risk_summary(self, risk_assessment: Dict) -> str:
        """构建风险评估摘要"""
        summary = []
        
        for assessor_name, assessment in risk_assessment.items():
            if isinstance(assessment, dict):
                risk_level = assessment.get("risk_level", "medium")
                risk_score = assessment.get("risk_score", 0.5)
                recommendation = assessment.get("recommendation", "建议观望")
                analysis = assessment.get("analysis", "风险评估完成")
                
                summary.append(f"**{assessor_name}：**")
                summary.append(f"- 风险等级：{risk_level}")
                summary.append(f"- 风险评分：{risk_score}")
                summary.append(f"- 建议：{recommendation}")
                summary.append(f"- 分析：{analysis}")
                summary.append("")
        
        return "\n".join(summary) if summary else "暂无风险评估数据"
    
    def _build_trading_summary(self, trading_decision: Dict) -> str:
        """构建交易决策摘要"""
        if not trading_decision:
            return "暂无交易决策数据"
        
        decision = trading_decision.get("decision", "观望")
        entry_price = trading_decision.get("entry_price", 0)
        stop_loss = trading_decision.get("stop_loss", 0)
        take_profit = trading_decision.get("take_profit", 0)
        confidence_score = trading_decision.get("confidence_score", 0.5)
        risk_score = trading_decision.get("risk_score", 0.5)
        
        summary = f"""决策：{decision}
入场价：{entry_price}
止损价：{stop_loss}
止盈价：{take_profit}
置信度：{confidence_score}
风险评分：{risk_score}"""
        
        return summary
    
    def _parse_risk_response(self, response: str, symbol: str) -> Dict[str, Any]:
        """解析风险经理响应"""
        try:
            # 提取最终决策
            if "最终风险决策:" in response:
                decision_part = response.split("最终风险决策:")[-1].strip()
                if "买入" in decision_part:
                    decision = "买入"
                elif "卖出" in decision_part:
                    decision = "卖出"
                elif "持有" in decision_part:
                    decision = "持有"
                else:
                    decision = "观望"
            else:
                decision = "观望"
            
            # 提取风险等级
            risk_level = "medium"
            if "高风险" in response or "high" in response.lower():
                risk_level = "high"
            elif "低风险" in response or "low" in response.lower():
                risk_level = "low"
            
            # 提取仓位建议
            position_size = 0.3  # 默认30%
            if "仓位" in response:
                import re
                position_match = re.search(r'仓位[：:]\s*(\d+(?:\.\d+)?)', response)
                if position_match:
                    try:
                        position_size = float(position_match.group(1)) / 100
                    except:
                        pass
            
            return {
                "final_decision": decision,
                "risk_level": risk_level,
                "position_size": position_size,
                "analysis": response,
                "symbol": symbol
            }
            
        except Exception as e:
            logger.error(f"解析风险响应失败: {e}")
            return self._generate_fallback_risk_decision(symbol)
    
    def _generate_fallback_risk_assessment(self, symbol: str) -> Dict[str, Any]:
        """生成备用风险评估"""
        return {
            "Aggressive Risk Assessor": {
                "risk_level": "medium",
                "risk_score": 0.5,
                "recommendation": "建议观望",
                "analysis": "数据不足，建议谨慎"
            },
            "Neutral Risk Assessor": {
                "risk_level": "medium",
                "risk_score": 0.5,
                "recommendation": "建议观望",
                "analysis": "数据不足，建议谨慎"
            },
            "Conservative Risk Assessor": {
                "risk_level": "medium",
                "risk_score": 0.5,
                "recommendation": "建议观望",
                "analysis": "数据不足，建议谨慎"
            }
        }
    
    def _generate_fallback_risk_decision(self, symbol: str) -> Dict[str, Any]:
        """生成备用风险决策"""
        return {
            "final_decision": "观望",
            "risk_level": "medium",
            "position_size": 0.2,
            "analysis": f"由于数据不足，建议对 {symbol} 保持观望态度",
            "symbol": symbol
        }


def create_risk_manager(llm, memory=None):
    """创建风险经理实例"""
    return RiskManager("Risk Manager")


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
    state.trading_decision = {
        "decision": "买入",
        "entry_price": 62000,
        "stop_loss": 61000,
        "take_profit": 64000,
        "confidence_score": 0.75,
        "risk_score": 0.4,
        "analysis": "基于技术分析建议买入",
        "symbol": "BTC/USDT"
    }
    state.analysis_reports = {
        "technical": {"summary": "BTC技术面显示上升趋势"},
        "fundamental": {"summary": "BTC基本面健康"},
        "news": {"summary": "市场情绪回暖"},
        "social": {"summary": "社交情绪积极"}
    }
    
    # 创建风险经理
    risk_manager = RiskManager()
    
    # 执行分析
    result = risk_manager.process(state)
    
    print("=== 风险经理测试结果 ===")
    print(f"最终决策: {result.final_risk_decision.get('final_decision', 'Unknown')}")
    print(f"风险等级: {result.final_risk_decision.get('risk_level', 'Unknown')}")
    print(f"建议仓位: {result.final_risk_decision.get('position_size', 0):.1%}") 