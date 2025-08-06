"""
AgentState 和 AgentMessage 定义
用于智能体之间的状态传递和消息通信
"""

from typing import Dict, Any, Optional
from dataclasses import dataclass, field
import json


@dataclass
class AgentMessage:
    """智能体消息类"""
    sender: str
    receiver: str
    message_type: str
    content: Dict[str, Any]
    timestamp: Optional[str] = None


class AgentState:
    """智能体状态管理类"""
    
    def __init__(self, symbol: str):
        self.symbol = symbol
        self.coin_name = symbol.split('/')[0] if '/' in symbol else symbol
        self.currency_name = symbol.split('/')[1] if '/' in symbol else "USDT"
        self.currency_symbol = self.currency_name
        
        # 分析报告存储
        self.analysis_reports: Dict[str, Any] = {
            "technical": None,
            "fundamental": None,
            "news": None,
            "social": None
        }
        
        # 研究共识
        self.research_consensus: Optional[Dict[str, Any]] = None
        
        # 交易决策
        self.trade_decision: Optional[Dict[str, Any]] = None
        
        # 风险评估
        self.risk_assessment: Optional[Dict[str, Any]] = None
        
        # 辩论历史
        self.debate_history: list = []
        
        # 最终输出
        self.final_output: Optional[Dict[str, Any]] = None
    
    def update_analysis_report(self, report_type: str, report_data: Dict[str, Any]):
        """更新分析报告"""
        self.analysis_reports[report_type] = report_data
    
    def add_debate_message(self, message: AgentMessage):
        """添加辩论消息"""
        self.debate_history.append(message)
    
    def get_all_analysis_reports(self) -> Dict[str, Any]:
        """获取所有分析报告"""
        return self.analysis_reports
    
    def to_dict(self) -> Dict[str, Any]:
        """转换为字典格式"""
        return {
            "symbol": self.symbol,
            "coin_name": self.coin_name,
            "currency_name": self.currency_name,
            "currency_symbol": self.currency_symbol,
            "analysis_reports": self.analysis_reports,
            "research_consensus": self.research_consensus,
            "trade_decision": self.trade_decision,
            "risk_assessment": self.risk_assessment,
            "debate_history": [msg.__dict__ for msg in self.debate_history],
            "final_output": self.final_output
        }
    
    def save_to_json(self, filepath: str):
        """保存状态到JSON文件"""
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(self.to_dict(), f, ensure_ascii=False, indent=2)


if __name__ == "__main__":
    # 独立测试
    state = AgentState("BTC/USDT")
    state.update_analysis_report("technical", {"trend": "bullish", "rsi": 65})
    state.update_analysis_report("fundamental", {"market_cap": 1000000000})
    
    print("AgentState 测试:")
    print(f"Symbol: {state.symbol}")
    print(f"Coin Name: {state.coin_name}")
    print(f"Analysis Reports: {state.analysis_reports}")
    
    # 测试消息
    message = AgentMessage(
        sender="Market Analyst",
        receiver="Research Manager", 
        message_type="analysis_report",
        content={"trend": "bullish"}
    )
    state.add_debate_message(message)
    
    print(f"Debate History: {len(state.debate_history)} messages")
    print("测试完成！") 