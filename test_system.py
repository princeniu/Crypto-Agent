"""
系统测试脚本
用于验证各个模块的功能
"""

import sys
import os
from utils.state import AgentState
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


def test_data_providers():
    """测试数据提供模块"""
    print("=== 测试数据提供模块 ===")
    
    try:
        from data_providers.market_data import MarketDataProvider
        provider = MarketDataProvider()
        market_data = provider.get_market_data("BTC/USDT")
        print(f"✅ 市场数据提供模块测试通过")
        print(f"   获取到 {len(market_data)} 条数据")
    except Exception as e:
        print(f"❌ 市场数据提供模块测试失败: {e}")
    
    try:
        from data_providers.fundamentals import FundamentalsDataProvider
        provider = FundamentalsDataProvider()
        fundamentals_data = provider.get_fundamentals_data("BTC")
        print(f"✅ 基本面数据提供模块测试通过")
        print(f"   获取到基本面数据")
    except Exception as e:
        print(f"❌ 基本面数据提供模块测试失败: {e}")
    
    try:
        from data_providers.news_data import NewsDataProvider
        provider = NewsDataProvider()
        news_data = provider.get_news_data("BTC")
        print(f"✅ 新闻数据提供模块测试通过")
        print(f"   获取到新闻数据")
    except Exception as e:
        print(f"❌ 新闻数据提供模块测试失败: {e}")
    
    try:
        from data_providers.social_data import SocialDataProvider
        provider = SocialDataProvider()
        social_data = provider.get_social_data("BTC")
        print(f"✅ 社交数据提供模块测试通过")
        print(f"   获取到社交数据")
    except Exception as e:
        print(f"❌ 社交数据提供模块测试失败: {e}")


def test_analysts():
    """测试分析师模块"""
    print("\n=== 测试分析师模块 ===")
    
    # 创建测试状态
    state = AgentState("BTC/USDT")
    
    try:
        from agents.analysts.market_analyst import MarketAnalyst
        analyst = MarketAnalyst()
        result_state = analyst.process(state)
        print(f"✅ 技术分析师测试通过")
    except Exception as e:
        print(f"❌ 技术分析师测试失败: {e}")
    
    try:
        from agents.analysts.fundamentals_analyst import FundamentalsAnalyst
        analyst = FundamentalsAnalyst()
        result_state = analyst.process(state)
        print(f"✅ 基本面分析师测试通过")
    except Exception as e:
        print(f"❌ 基本面分析师测试失败: {e}")
    
    try:
        from agents.analysts.news_analyst import NewsAnalyst
        analyst = NewsAnalyst()
        result_state = analyst.process(state)
        print(f"✅ 新闻分析师测试通过")
    except Exception as e:
        print(f"❌ 新闻分析师测试失败: {e}")
    
    try:
        from agents.analysts.social_media_analyst import SocialMediaAnalyst
        analyst = SocialMediaAnalyst()
        result_state = analyst.process(state)
        print(f"✅ 社交媒体分析师测试通过")
    except Exception as e:
        print(f"❌ 社交媒体分析师测试失败: {e}")


def test_researchers():
    """测试研究员模块"""
    print("\n=== 测试研究员模块 ===")
    
    # 创建测试状态
    state = AgentState("BTC/USDT")
    
    # 模拟分析报告
    state.update_analysis_report("technical", {
        "analyst": "Market Analyst",
        "analysis": "BTC技术面显示多头趋势，RSI为65，MACD金叉。"
    })
    
    state.update_analysis_report("fundamental", {
        "analyst": "Fundamentals Analyst", 
        "analysis": "BTC基本面强劲，市值排名第一。"
    })
    
    state.update_analysis_report("news", {
        "analyst": "News Analyst",
        "analysis": "近期新闻情绪正面，机构投资增加。"
    })
    
    state.update_analysis_report("social", {
        "analyst": "Social Media Analyst",
        "analysis": "社交媒体情绪积极，用户情绪偏向乐观。"
    })
    
    try:
        from agents.researchers.bull_researcher import BullResearcher
        researcher = BullResearcher()
        result_state = researcher.process(state)
        print(f"✅ 看涨研究员测试通过")
    except Exception as e:
        print(f"❌ 看涨研究员测试失败: {e}")
    
    try:
        from agents.researchers.bear_researcher import BearResearcher
        researcher = BearResearcher()
        result_state = researcher.process(state)
        print(f"✅ 看跌研究员测试通过")
    except Exception as e:
        print(f"❌ 看跌研究员测试失败: {e}")


def test_managers():
    """测试管理层模块"""
    print("\n=== 测试管理层模块 ===")
    
    # 创建测试状态
    state = AgentState("BTC/USDT")
    
    # 模拟分析报告和研究共识
    state.update_analysis_report("technical", {
        "analyst": "Market Analyst",
        "analysis": "BTC技术面显示多头趋势，RSI为65，MACD金叉。"
    })
    
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
    
    try:
        from agents.managers.research_manager import ResearchManager
        manager = ResearchManager()
        result_state = manager.process(state)
        print(f"✅ 研究经理测试通过")
    except Exception as e:
        print(f"❌ 研究经理测试失败: {e}")


def test_config():
    """测试配置模块"""
    print("\n=== 测试配置模块 ===")
    
    try:
        print(f"OpenAI模型: {Config.OPENAI_MODEL}")
        print(f"交易所: {Config.EXCHANGE_NAME}")
        print(f"输出目录: {Config.OUTPUT_DIR}")
        
        is_valid = Config.validate_config()
        if is_valid:
            print("✅ 配置验证通过")
        else:
            print("⚠️ 配置验证失败，请检查 .env 文件")
            
    except Exception as e:
        print(f"❌ 配置模块测试失败: {e}")


def main():
    """主测试函数"""
    print("🚀 开始系统测试...\n")
    
    # 测试配置
    test_config()
    
    # 测试数据提供模块
    test_data_providers()
    
    # 测试分析师模块
    test_analysts()
    
    # 测试研究员模块
    test_researchers()
    
    # 测试管理层模块
    test_managers()
    
    print("\n✅ 系统测试完成！")


if __name__ == "__main__":
    main() 