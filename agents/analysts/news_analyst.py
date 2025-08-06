"""
新闻分析师
基于CryptoPanic等新闻数据生成新闻分析报告
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from typing import Dict, Any
from agents.analysts.base import BaseAnalyst
from utils.state import AgentState
from utils.logger import get_logger
from data_providers.news_data import NewsDataProvider

logger = get_logger(__name__)


class NewsAnalyst(BaseAnalyst):
    """新闻分析师"""
    
    def __init__(self, name: str = "News Analyst"):
        super().__init__(name)
        self.news_provider = NewsDataProvider()
    
    def process(self, state: AgentState) -> AgentState:
        """处理新闻分析"""
        try:
            logger.info(f"{self.name} 开始分析 {state.symbol}")
            
            # 获取新闻数据
            news_data = self.news_provider.get_news_data(state.coin_name)
            
            if not news_data:
                logger.error(f"无法获取 {state.coin_name} 的新闻数据")
                return state
            
            # 生成新闻分析报告
            analysis_result = self._generate_news_analysis(state, news_data)
            
            # 更新状态
            self.update_state_with_analysis(state, "news", analysis_result)
            
            logger.info(f"{self.name} 完成 {state.symbol} 新闻分析")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 分析失败: {e}")
            return state
    
    def _generate_news_analysis(self, state: AgentState, news_data: Dict[str, Any]) -> str:
        """生成新闻分析报告"""
        
        # 构建分析提示词
        prompt = self._create_news_analysis_prompt(state, news_data)
        
        # 调用LLM生成分析
        analysis = self.call_llm(prompt)
        
        return analysis
    
    def _create_news_analysis_prompt(self, state: AgentState, news_data: Dict[str, Any]) -> str:
        """创建新闻分析提示词"""
        
        coin_news = news_data.get('coin_news', [])
        general_news = news_data.get('general_news', [])
        coin_sentiment = news_data.get('coin_sentiment', {})
        general_sentiment = news_data.get('general_sentiment', {})
        analysis_summary = news_data.get('analysis_summary', {})
        
        # 提取关键新闻标题
        coin_news_titles = [news.get('title', '') for news in coin_news[:5]]
        general_news_titles = [news.get('title', '') for news in general_news[:5]]
        
        # 情绪数据
        coin_sentiment_score = coin_sentiment.get('sentiment_score', 0)
        general_sentiment_score = general_sentiment.get('sentiment_score', 0)
        overall_sentiment = analysis_summary.get('overall_sentiment', 0)
        
        # 统计信息
        total_coin_news = analysis_summary.get('total_coin_news', 0)
        total_general_news = analysis_summary.get('total_general_news', 0)
        
        prompt = f"""
你是一位专业的加密货币新闻分析师。

分析目标：{state.coin_name}（交易对：{state.symbol}）

📰 币种相关新闻（共{total_coin_news}条）：
{chr(10).join([f"- {title}" for title in coin_news_titles])}

📰 市场整体新闻（共{total_general_news}条）：
{chr(10).join([f"- {title}" for title in general_news_titles])}

📊 新闻情绪分析：
- 币种相关新闻情绪得分：{coin_sentiment_score:.3f} (-1到1，正值表示正面)
- 市场整体新闻情绪得分：{general_sentiment_score:.3f}
- 综合情绪得分：{overall_sentiment:.3f}

📈 情绪统计：
- 币种正面新闻：{coin_sentiment.get('positive_count', 0)}条
- 币种负面新闻：{coin_sentiment.get('negative_count', 0)}条
- 币种中性新闻：{coin_sentiment.get('neutral_count', 0)}条

请基于以上真实新闻数据进行新闻分析，生成完整的中文新闻分析报告，包括：

## 📰 新闻概览
- 币种相关新闻数量与质量
- 市场整体新闻环境
- 重要新闻事件梳理

## 📊 情绪分析
- 币种相关新闻情绪解读
- 市场整体情绪趋势
- 情绪对价格的影响分析

## 🔍 事件影响评估
- 重要新闻事件对币种的影响
- 市场整体新闻对币种的影响
- 短期和长期影响预测

## 💭 投资建议
- 基于新闻情绪的投资建议（买入/持有/卖出，中文表达）
- 风险提示与注意事项
- 需要关注的后续新闻事件

要求：
- 所有分析必须基于提供的真实新闻数据
- 投资建议必须使用中文（买入/持有/卖出）
- 报告长度不少于600字
- 分析要具体、专业、有说服力
- 重点关注新闻对价格走势的影响
"""

        return prompt


def create_news_analyst(llm=None, memory=None):
    """创建新闻分析师实例"""
    return NewsAnalyst("News Analyst")


if __name__ == "__main__":
    # 独立测试
    print("=== 新闻分析师独立测试 ===")
    
    # 创建状态
    state = AgentState("BTC/USDT")
    
    # 创建分析师
    analyst = NewsAnalyst()
    
    # 执行分析
    result_state = analyst.process(state)
    
    # 输出结果
    print(f"\n分析完成！")
    print(f"币种: {result_state.symbol}")
    
    news_report = result_state.analysis_reports.get("news")
    if news_report:
        print(f"\n新闻分析报告:")
        print(f"分析师: {news_report.get('analyst', 'Unknown')}")
        print(f"分析内容: {news_report.get('analysis', 'No analysis')[:200]}...")
    else:
        print("未生成新闻分析报告")
    
    print("\n测试完成！") 