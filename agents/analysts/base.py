"""
分析师基类
定义所有分析师的基础接口和通用方法
"""

from abc import ABC, abstractmethod
from typing import Dict, Any
import openai
import pandas as pd
from utils.state import AgentState
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class BaseAnalyst(ABC):
    """分析师基类"""
    
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
    
    def create_analysis_prompt(self, state: AgentState, data: Dict[str, Any]) -> str:
        """创建分析提示词"""
        return f"""
请作为{self.name}，对{state.coin_name}（{state.symbol}）进行分析。

可用数据：
{data}

请提供详细的分析报告，包括：
1. 数据解读
2. 趋势分析
3. 投资建议

请用中文回答，确保分析基于提供的数据。
"""
    
    def update_state_with_analysis(self, state: AgentState, analysis_type: str, analysis_result: str):
        """更新状态中的分析报告"""
        state.update_analysis_report(analysis_type, {
            "analyst": self.name,
            "analysis": analysis_result,
            "timestamp": str(pd.Timestamp.now())
        })
        logger.info(f"{self.name} 完成 {analysis_type} 分析")


def create_analyst(analyst_class: type, name: str) -> BaseAnalyst:
    """创建分析师实例的工厂函数"""
    return analyst_class(name)


if __name__ == "__main__":
    # 独立测试
    print("分析师基类测试:")
    
    # 测试状态创建
    from utils.state import AgentState
    state = AgentState("BTC/USDT")
    
    print(f"创建状态: {state.symbol}")
    print(f"币种名称: {state.coin_name}")
    print(f"货币名称: {state.currency_name}")
    
    # 测试配置
    from utils.config import Config
    print(f"OpenAI模型: {Config.OPENAI_MODEL}")
    print(f"交易所: {Config.EXCHANGE_NAME}")
    
    print("基类测试完成！") 