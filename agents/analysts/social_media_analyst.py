"""
社交媒体分析师
基于Reddit等社交数据生成社交情绪分析报告
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))

from typing import Dict, Any
from agents.analysts.base import BaseAnalyst
from utils.state import AgentState
from utils.logger import get_logger
from data_providers.social_data import SocialDataProvider

logger = get_logger(__name__)


class SocialMediaAnalyst(BaseAnalyst):
    """社交媒体分析师"""
    
    def __init__(self, name: str = "Social Media Analyst"):
        super().__init__(name)
        self.social_provider = SocialDataProvider()
    
    def process(self, state: AgentState) -> AgentState:
        """处理社交分析"""
        try:
            logger.info(f"{self.name} 开始分析 {state.symbol}")
            
            # 获取社交数据
            social_data = self.social_provider.get_social_data(state.coin_name)
            
            if not social_data:
                logger.error(f"无法获取 {state.coin_name} 的社交数据")
                return state
            
            # 生成社交分析报告
            analysis_result = self._generate_social_analysis(state, social_data)
            
            # 更新状态
            self.update_state_with_analysis(state, "social", analysis_result)
            
            logger.info(f"{self.name} 完成 {state.symbol} 社交分析")
            return state
            
        except Exception as e:
            logger.error(f"{self.name} 分析失败: {e}")
            return state
    
    def _generate_social_analysis(self, state: AgentState, social_data: Dict[str, Any]) -> str:
        """生成社交分析报告"""
        
        # 构建分析提示词
        prompt = self._create_social_analysis_prompt(state, social_data)
        
        # 调用LLM生成分析
        analysis = self.call_llm(prompt)
        
        return analysis
    
    def _create_social_analysis_prompt(self, state: AgentState, social_data: Dict[str, Any]) -> str:
        """创建社交分析提示词"""
        
        reddit_posts = social_data.get('reddit_posts', [])
        sentiment_analysis = social_data.get('sentiment_analysis', {})
        analysis_summary = social_data.get('analysis_summary', {})
        
        # 提取关键帖子标题
        post_titles = [post.get('title', '') for post in reddit_posts[:5]]
        
        # 情绪数据
        sentiment_score = sentiment_analysis.get('sentiment_score', 0)
        positive_count = sentiment_analysis.get('positive_count', 0)
        negative_count = sentiment_analysis.get('negative_count', 0)
        neutral_count = sentiment_analysis.get('neutral_count', 0)
        total_count = sentiment_analysis.get('total_count', 0)
        
        # 热度数据
        total_score = analysis_summary.get('total_score', 0)
        total_comments = analysis_summary.get('total_comments', 0)
        avg_score = sentiment_analysis.get('avg_score', 0)
        avg_upvote_ratio = sentiment_analysis.get('avg_upvote_ratio', 0)
        engagement_rate = analysis_summary.get('engagement_rate', 0)
        
        prompt = f"""
你是一位专业的加密货币社交媒体分析师。

分析目标：{state.coin_name}（交易对：{state.symbol}）

📱 社交媒体数据概览：
- 总帖子数量：{total_count}条
- 总评分：{total_score}
- 总评论数：{total_comments}
- 平均评分：{avg_score:.2f}
- 平均点赞率：{avg_upvote_ratio:.3f}
- 参与度：{engagement_rate:.2f}

📊 情绪分析：
- 整体情绪得分：{sentiment_score:.3f} (-1到1，正值表示正面)
- 正面帖子：{positive_count}条
- 负面帖子：{negative_count}条
- 中性帖子：{neutral_count}条

📝 热门帖子标题：
{chr(10).join([f"- {title}" for title in post_titles])}

请基于以上真实社交媒体数据进行社交情绪分析，生成完整的中文社交分析报告，包括：

## 📱 社交媒体概览
- Reddit等平台讨论热度
- 用户参与度与活跃度
- 社区讨论质量分析

## 📊 情绪趋势分析
- 社交媒体情绪解读
- 用户情绪变化趋势
- 情绪对价格的影响分析

## 🔍 社区行为分析
- 用户讨论焦点与热点话题
- 社区反应与情绪波动
- 社交媒体对市场的影响

## 💭 投资建议
- 基于社交情绪的投资建议（买入/持有/卖出，中文表达）
- 社交媒体风险提示
- 需要关注的社区动态

要求：
- 所有分析必须基于提供的真实社交数据
- 投资建议必须使用中文（买入/持有/卖出）
- 报告长度不少于600字
- 分析要具体、专业、有说服力
- 重点关注社交媒体情绪对价格走势的影响
"""

        return prompt


def create_social_media_analyst(llm=None, memory=None):
    """创建社交媒体分析师实例"""
    return SocialMediaAnalyst("Social Media Analyst")


if __name__ == "__main__":
    # 独立测试
    print("=== 社交媒体分析师独立测试 ===")
    
    # 创建状态
    state = AgentState("BTC/USDT")
    
    # 创建分析师
    analyst = SocialMediaAnalyst()
    
    # 执行分析
    result_state = analyst.process(state)
    
    # 输出结果
    print(f"\n分析完成！")
    print(f"币种: {result_state.symbol}")
    
    social_report = result_state.analysis_reports.get("social")
    if social_report:
        print(f"\n社交分析报告:")
        print(f"分析师: {social_report.get('analyst', 'Unknown')}")
        print(f"分析内容: {social_report.get('analysis', 'No analysis')[:200]}...")
    else:
        print("未生成社交分析报告")
    
    print("\n测试完成！") 