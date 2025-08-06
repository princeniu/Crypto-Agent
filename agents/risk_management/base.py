"""
风险管理基类
定义所有风险管理智能体的基础接口和通用方法
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import openai
import pandas as pd
from utils.state import AgentState
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseRiskManager(ABC):
    """风险管理基类"""
    
    def __init__(self, name: str):
        self.name = name
        self.client = None
        self._init_openai()
    
    def _init_openai(self):
        """初始化OpenAI客户端"""
        try:
            if Config.OPENAI_API_KEY:
                self.client = openai.OpenAI(api_key=Config.OPENAI_API_KEY)
                logger.info(f"{self.name} OpenAI客户端初始化成功")
            else:
                logger.warning(f"{self.name} OpenAI API密钥未设置")
        except Exception as e:
            logger.error(f"{self.name} OpenAI客户端初始化失败: {e}")
    
    @abstractmethod
    def process(self, state: AgentState) -> AgentState:
        """
        处理输入状态并返回更新后的状态
        
        Args:
            state: 当前智能体状态
            
        Returns:
            更新后的智能体状态
        """
        pass
    
    def call_llm(self, prompt: str, temperature: float = None) -> str:
        """调用LLM获取分析结果"""
        try:
            if not self.client:
                logger.error("OpenAI客户端未初始化")
                return "无法获取分析结果，OpenAI客户端未初始化"
            
            response = self.client.chat.completions.create(
                model=Config.OPENAI_MODEL,
                messages=[{"role": "user", "content": prompt}],
                temperature=temperature or Config.OPENAI_TEMPERATURE,
                max_tokens=2000
            )
            
            return response.choices[0].message.content
            
        except Exception as e:
            logger.error(f"调用LLM失败: {e}")
            return f"分析过程中出现错误: {str(e)}"
    
    def get_analysis_reports(self, state: AgentState) -> Dict[str, Any]:
        """获取所有分析报告"""
        return state.get_all_analysis_reports()
    
    def get_research_consensus(self, state: AgentState) -> Dict[str, Any]:
        """获取研究共识"""
        return state.research_consensus or {}
    
    def get_trade_decision(self, state: AgentState) -> Dict[str, Any]:
        """获取交易决策"""
        return state.trade_decision or {}


def create_risk_manager(risk_manager_class: type, name: str) -> BaseRiskManager:
    """创建风险管理实例的工厂函数"""
    return risk_manager_class(name)


if __name__ == "__main__":
    # 独立测试
    print("风险管理基类测试:")
    
    # 测试状态创建
    from utils.state import AgentState
    state = AgentState("BTC/USDT")
    
    print(f"创建状态: {state.symbol}")
    print(f"币种名称: {state.coin_name}")
    print(f"货币名称: {state.currency_name}")
    
    # 测试配置
    from utils.config import Config
    print(f"OpenAI模型: {Config.OPENAI_MODEL}")
    
    print("基类测试完成！") 