"""
模块独立性测试脚本
测试各个智能体模块的独立运行能力
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from utils.config import Config
from utils.state import AgentState

def test_analysts():
    """测试分析师模块"""
    print("=== 测试分析师模块 ===")
    
    # 测试技术分析师
    try:
        from agents.analysts.market_analyst import MarketAnalyst
        analyst = MarketAnalyst("Market Analyst")
        state = AgentState("BTC/USDT")
        result = analyst.process(state)
        print("✅ 技术分析师测试通过")
    except Exception as e:
        print(f"❌ 技术分析师测试失败: {e}")
    
    # 测试基本面分析师
    try:
        from agents.analysts.fundamentals_analyst import FundamentalsAnalyst
        analyst = FundamentalsAnalyst("Fundamentals Analyst")
        state = AgentState("BTC/USDT")
        result = analyst.process(state)
        print("✅ 基本面分析师测试通过")
    except Exception as e:
        print(f"❌ 基本面分析师测试失败: {e}")

def test_researchers():
    """测试研究员模块"""
    print("\n=== 测试研究员模块 ===")
    
    # 测试看涨研究员
    try:
        from agents.researchers.bull_researcher import BullResearcher
        researcher = BullResearcher("Bull Researcher")
        state = AgentState("BTC/USDT")
        state.analysis_reports = {
            "technical": {"summary": "技术面看涨"},
            "fundamental": {"summary": "基本面健康"},
            "news": {"summary": "新闻利好"},
            "social": {"summary": "社交情绪积极"}
        }
        result = researcher.process(state)
        print("✅ 看涨研究员测试通过")
    except Exception as e:
        print(f"❌ 看涨研究员测试失败: {e}")
    
    # 测试看跌研究员
    try:
        from agents.researchers.bear_researcher import BearResearcher
        researcher = BearResearcher("Bear Researcher")
        state = AgentState("BTC/USDT")
        state.analysis_reports = {
            "technical": {"summary": "技术面看跌"},
            "fundamental": {"summary": "基本面疲软"},
            "news": {"summary": "新闻利空"},
            "social": {"summary": "社交情绪消极"}
        }
        result = researcher.process(state)
        print("✅ 看跌研究员测试通过")
    except Exception as e:
        print(f"❌ 看跌研究员测试失败: {e}")

def test_trader():
    """测试交易员模块"""
    print("\n=== 测试交易员模块 ===")
    
    try:
        from agents.trader.trader import Trader
        trader = Trader("Trader")
        state = AgentState("BTC/USDT")
        state.analysis_reports = {
            "technical": {"summary": "技术面显示上升趋势"},
            "fundamental": {"summary": "基本面健康"},
            "news": {"summary": "新闻利好"},
            "social": {"summary": "社交情绪积极"}
        }
        state.research_consensus = {
            "manager_consensus": {
                "consensus": "综合看涨，建议买入"
            }
        }
        result = trader.process(state)
        print("✅ 交易员测试通过")
    except Exception as e:
        print(f"❌ 交易员测试失败: {e}")

def test_risk_management():
    """测试风险管理模块"""
    print("\n=== 测试风险管理模块 ===")
    
    try:
        from agents.managers.risk_manager import RiskManager
        risk_manager = RiskManager("Risk Manager")
        state = AgentState("BTC/USDT")
        state.trading_decision = {
            "decision": "买入",
            "entry_price": 62000,
            "stop_loss": 61000,
            "take_profit": 64000,
            "confidence_score": 0.75,
            "risk_score": 0.4
        }
        state.analysis_reports = {
            "technical": {"summary": "技术面健康"},
            "fundamental": {"summary": "基本面良好"},
            "news": {"summary": "新闻中性"},
            "social": {"summary": "社交情绪稳定"}
        }
        result = risk_manager.process(state)
        print("✅ 风险管理测试通过")
    except Exception as e:
        print(f"❌ 风险管理测试失败: {e}")

def test_managers():
    """测试管理层模块"""
    print("\n=== 测试管理层模块 ===")
    
    try:
        from agents.managers.research_manager import ResearchManager
        manager = ResearchManager("Research Manager")
        state = AgentState("BTC/USDT")
        state.analysis_reports = {
            "technical": {"analysis": "技术分析数据"},
            "fundamental": {"analysis": "基本面分析数据"},
            "news": {"analysis": "新闻分析数据"},
            "social": {"analysis": "社交分析数据"}
        }
        state.research_consensus = {
            "bull_analysis": {"analysis": "看涨分析"},
            "bear_analysis": {"analysis": "看跌分析"}
        }
        result = manager.process(state)
        print("✅ 研究经理测试通过")
    except Exception as e:
        print(f"❌ 研究经理测试失败: {e}")

def main():
    """主测试函数"""
    print("🚀 开始模块独立性测试...")
    
    # 验证配置
    if not Config.validate_config():
        print("❌ 配置验证失败，请检查 .env 文件")
        return
    
    # 测试各个模块
    test_analysts()
    test_researchers()
    test_trader()
    test_risk_management()
    test_managers()
    
    print("\n🎉 所有模块测试完成！")

if __name__ == "__main__":
    main() 