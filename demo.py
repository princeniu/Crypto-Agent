"""
AI加密货币多智能体专家系统 - 演示脚本
展示系统的完整功能
"""

import sys
import os
import json
from utils.state import AgentState
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


def demo_data_providers():
    """演示数据提供模块"""
    print("🔍 演示数据提供模块...")
    
    try:
        from data_providers.market_data import MarketDataProvider
        provider = MarketDataProvider()
        market_data = provider.get_market_data("BTC/USDT")
        
        if market_data:
            print(f"✅ 市场数据获取成功")
            print(f"   当前价格: ${market_data.get('current_price', 0):,.2f}")
            print(f"   24小时涨跌幅: {market_data.get('price_change_24h', 0):.2f}%")
            print(f"   趋势: {market_data.get('trend', 'unknown')}")
            print(f"   RSI: {market_data.get('technical_indicators', {}).get('rsi', 0):.2f}")
        else:
            print("❌ 市场数据获取失败")
            
    except Exception as e:
        print(f"❌ 市场数据演示失败: {e}")
    
    try:
        from data_providers.fundamentals import FundamentalsDataProvider
        provider = FundamentalsDataProvider()
        fundamentals_data = provider.get_fundamentals_data("BTC")
        
        if fundamentals_data:
            analysis = fundamentals_data.get('analysis_summary', {})
            print(f"✅ 基本面数据获取成功")
            print(f"   市值排名: {analysis.get('market_cap_rank', 'N/A')}")
            print(f"   市值: ${analysis.get('market_cap', 0):,.0f}")
            print(f"   24小时成交量: ${analysis.get('volume_24h', 0):,.0f}")
        else:
            print("❌ 基本面数据获取失败")
            
    except Exception as e:
        print(f"❌ 基本面数据演示失败: {e}")


def demo_analysts():
    """演示分析师模块"""
    print("\n📊 演示分析师模块...")
    
    # 创建测试状态
    state = AgentState("BTC/USDT")
    
    try:
        from agents.analysts.market_analyst import MarketAnalyst
        analyst = MarketAnalyst()
        result_state = analyst.process(state)
        
        technical_report = result_state.analysis_reports.get("technical")
        if technical_report:
            print(f"✅ 技术分析师分析完成")
            print(f"   分析师: {technical_report.get('analyst', 'Unknown')}")
            analysis = technical_report.get('analysis', 'No analysis')
            print(f"   分析内容: {analysis[:100]}...")
        else:
            print("❌ 技术分析师分析失败")
            
    except Exception as e:
        print(f"❌ 技术分析师演示失败: {e}")
    
    try:
        from agents.analysts.fundamentals_analyst import FundamentalsAnalyst
        analyst = FundamentalsAnalyst()
        result_state = analyst.process(state)
        
        fundamental_report = result_state.analysis_reports.get("fundamental")
        if fundamental_report:
            print(f"✅ 基本面分析师分析完成")
            print(f"   分析师: {fundamental_report.get('analyst', 'Unknown')}")
            analysis = fundamental_report.get('analysis', 'No analysis')
            print(f"   分析内容: {analysis[:100]}...")
        else:
            print("❌ 基本面分析师分析失败")
            
    except Exception as e:
        print(f"❌ 基本面分析师演示失败: {e}")


def demo_researchers():
    """演示研究员模块"""
    print("\n🤝 演示研究员模块...")
    
    # 创建测试状态
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
    
    try:
        from agents.researchers.bull_researcher import BullResearcher
        researcher = BullResearcher()
        result_state = researcher.process(state)
        
        research_consensus = result_state.research_consensus
        if research_consensus:
            bull_analysis = research_consensus.get("bull_analysis", {})
            print(f"✅ 看涨研究员分析完成")
            print(f"   研究员: {bull_analysis.get('researcher', 'Unknown')}")
            analysis = bull_analysis.get('analysis', 'No analysis')
            print(f"   分析内容: {analysis[:100]}...")
        else:
            print("❌ 看涨研究员分析失败")
            
    except Exception as e:
        print(f"❌ 看涨研究员演示失败: {e}")
    
    try:
        from agents.researchers.bear_researcher import BearResearcher
        researcher = BearResearcher()
        result_state = researcher.process(state)
        
        research_consensus = result_state.research_consensus
        if research_consensus:
            bear_analysis = research_consensus.get("bear_analysis", {})
            print(f"✅ 看跌研究员分析完成")
            print(f"   研究员: {bear_analysis.get('researcher', 'Unknown')}")
            analysis = bear_analysis.get('analysis', 'No analysis')
            print(f"   分析内容: {analysis[:100]}...")
        else:
            print("❌ 看跌研究员分析失败")
            
    except Exception as e:
        print(f"❌ 看跌研究员演示失败: {e}")


def demo_managers():
    """演示管理层模块"""
    print("\n👨‍💼 演示管理层模块...")
    
    # 创建测试状态
    state = AgentState("BTC/USDT")
    
    # 模拟分析报告和研究共识
    state.update_analysis_report("technical", {
        "analyst": "Market Analyst",
        "analysis": "BTC技术面显示多头趋势，RSI为65，MACD金叉，布林带显示价格在上升通道中。"
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
        
        research_consensus = result_state.research_consensus
        if research_consensus:
            manager_consensus = research_consensus.get("manager_consensus", {})
            print(f"✅ 研究经理决策完成")
            print(f"   经理: {manager_consensus.get('manager', 'Unknown')}")
            consensus = manager_consensus.get('consensus', 'No consensus')
            print(f"   决策内容: {consensus[:100]}...")
        else:
            print("❌ 研究经理决策失败")
            
    except Exception as e:
        print(f"❌ 研究经理演示失败: {e}")


def demo_complete_system():
    """演示完整系统"""
    print("\n🚀 演示完整系统...")
    
    try:
        from main import CryptoAgentSystem
        system = CryptoAgentSystem()
        
        # 运行分析（不依赖OpenAI）
        print("正在运行完整分析流程...")
        results = system.run_analysis("BTC/USDT")
        
        if "error" not in results:
            print(f"✅ 完整系统演示成功")
            print(f"   币种: {results.get('symbol', 'Unknown')}")
            print(f"   趋势: {results.get('trend', 'Unknown')}")
            print(f"   置信度: {results.get('confidence_score', 0):.2f}")
            print(f"   风险等级: {results.get('risk_level', 'Unknown')}")
        else:
            print(f"❌ 完整系统演示失败: {results.get('error', 'Unknown error')}")
            
    except Exception as e:
        print(f"❌ 完整系统演示失败: {e}")


def main():
    """主演示函数"""
    print("🎯 AI加密货币多智能体专家系统演示")
    print("=" * 50)
    
    # 演示数据提供模块
    demo_data_providers()
    
    # 演示分析师模块
    demo_analysts()
    
    # 演示研究员模块
    demo_researchers()
    
    # 演示管理层模块
    demo_managers()
    
    # 演示完整系统
    demo_complete_system()
    
    print("\n" + "=" * 50)
    print("✅ 演示完成！")
    print("\n📝 使用说明:")
    print("1. 配置 .env 文件中的 OpenAI API 密钥")
    print("2. 运行 python main.py 进行完整分析")
    print("3. 运行 python test_system.py 进行系统测试")
    print("4. 查看 output/results.json 获取分析结果")


if __name__ == "__main__":
    main() 