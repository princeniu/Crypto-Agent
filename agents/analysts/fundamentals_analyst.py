"""
基本面分析师
基于CoinGecko等数据生成基本面分析报告
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from typing import Dict, Any
from agents.analysts.base import BaseAnalyst
from utils.state import AgentState
from utils.logger import get_logger
from data_providers.fundamentals import FundamentalsDataProvider

logger = get_logger(__name__)


class FundamentalsAnalyst(BaseAnalyst):
    """基本面分析师"""
    
    def __init__(self, name: str = "Fundamentals Analyst"):
        super().__init__(name)
        self.fundamentals_provider = FundamentalsDataProvider()
    
    def process(self, state: AgentState) -> AgentState:
        """处理基本面分析"""
        try:
            logger.info(f"{self.name} 开始分析 {state.symbol}")
            
            # 获取基本面数据
            fundamentals_data = self.fundamentals_provider.get_fundamentals_data(state.coin_name)
            
            if not fundamentals_data:
                logger.error(f"无法获取 {state.coin_name} 的基本面数据")
                return state
            
            # 生成基本面分析报告
            analysis_result = self._generate_fundamentals_analysis(state, fundamentals_data)
            
            # 更新状态
            self.update_state_with_analysis(state, "fundamental", analysis_result)
            
            logger.info(f"{self.name} 完成 {state.symbol} 基本面分析")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 分析失败: {e}")
            return state
    
    def _generate_fundamentals_analysis(self, state: AgentState, fundamentals_data: Dict[str, Any]) -> str:
        """生成基本面分析报告"""
        
        # 构建分析提示词
        prompt = self._create_fundamentals_analysis_prompt(state, fundamentals_data)
        
        # 调用LLM生成分析
        analysis = self.call_llm(prompt)
        
        return analysis
    
    def _create_fundamentals_analysis_prompt(self, state: AgentState, fundamentals_data: Dict[str, Any]) -> str:
        """创建基本面分析提示词"""
        
        coin_info = fundamentals_data.get('coin_info', {})
        analysis_summary = fundamentals_data.get('analysis_summary', {})
        
        market_cap = analysis_summary.get('market_cap', 0)
        market_cap_rank = analysis_summary.get('market_cap_rank', 'N/A')
        volume_24h = analysis_summary.get('volume_24h', 0)
        circulating_supply = analysis_summary.get('circulating_supply', 0)
        price_change_24h = analysis_summary.get('price_change_24h', 0)
        community_score = analysis_summary.get('community_score', 0)
        developer_score = analysis_summary.get('developer_score', 0)
        trust_score = analysis_summary.get('trust_score', 0)
        
        # 获取更多详细信息
        total_supply = coin_info.get('total_supply', 0)
        max_supply = coin_info.get('max_supply', 0)
        ath = coin_info.get('ath', 0)
        ath_change_percentage = coin_info.get('ath_change_percentage', 0)
        atl = coin_info.get('atl', 0)
        atl_change_percentage = coin_info.get('atl_change_percentage', 0)
        description = coin_info.get('description', '')
        categories = coin_info.get('categories', [])
        
        prompt = f"""
你是一位专业的加密货币基本面分析师。

分析目标：{state.coin_name}（交易对：{state.symbol}）

📊 基本面数据：
- 市值排名：{market_cap_rank}
- 市值：${market_cap:,.0f}
- 24小时成交量：${volume_24h:,.0f}
- 流通供应量：{circulating_supply:,.0f}
- 总供应量：{total_supply:,.0f}
- 最大供应量：{max_supply:,.0f}
- 24小时涨跌幅：{price_change_24h:.2f}%

📈 历史价格数据：
- 历史最高价：${ath:,.2f} (距离当前价格: {ath_change_percentage:.2f}%)
- 历史最低价：${atl:,.2f} (距离当前价格: {atl_change_percentage:.2f}%)

🏆 项目评分：
- 社区评分：{community_score}/100
- 开发者评分：{developer_score}/100
- 信任评分：{trust_score}/100

📋 项目信息：
- 项目描述：{description[:500]}...
- 项目分类：{', '.join(categories) if categories else '未分类'}

请基于以上真实数据进行基本面分析，生成完整的中文基本面分析报告，包括：

## 📊 项目基本信息
- 币种名称：{state.coin_name}
- 市值排名与规模分析
- 供应量结构与代币经济模型

## 📈 基本面指标分析
- 市值、成交量、流通量分析
- 历史价格表现与当前估值水平
- 项目评分与社区活跃度

## 🔹 项目价值评估
- 项目定位与竞争优势
- 技术实力与开发活跃度
- 社区建设与用户基础

## 💭 投资价值分析
- 长期投资价值评估
- 风险因素分析
- 投资建议（买入/持有/卖出，中文表达）

要求：
- 所有分析必须基于提供的真实数据
- 投资建议必须使用中文（买入/持有/卖出）
- 报告长度不少于600字
- 分析要具体、专业、有说服力
- 重点关注项目的长期价值和发展潜力
"""

        return prompt


def create_fundamentals_analyst(llm=None, memory=None):
    """创建基本面分析师实例"""
    return FundamentalsAnalyst("Fundamentals Analyst")


if __name__ == "__main__":
    # 独立测试
    print("=== 基本面分析师独立测试 ===")
    
    # 创建状态
    state = AgentState("BTC/USDT")
    
    # 创建分析师
    analyst = FundamentalsAnalyst()
    
    # 执行分析
    result_state = analyst.process(state)
    
    # 输出结果
    print(f"\n分析完成！")
    print(f"币种: {result_state.symbol}")
    
    fundamental_report = result_state.analysis_reports.get("fundamental")
    if fundamental_report:
        print(f"\n基本面分析报告:")
        print(f"分析师: {fundamental_report.get('analyst', 'Unknown')}")
        print(f"分析内容: {fundamental_report.get('analysis', 'No analysis')[:200]}...")
    else:
        print("未生成基本面分析报告")
    
    print("\n测试完成！") 