"""
AI加密货币多智能体专家系统 - 主入口
串联所有智能体完成完整的加密货币分析流程
"""

import sys
import os
import json
import pandas as pd
from typing import Dict, Any
from utils.state import AgentState
from utils.config import Config
from utils.logger import get_logger

# 导入智能体
from agents.analysts.market_analyst import MarketAnalyst
from agents.analysts.fundamentals_analyst import FundamentalsAnalyst
from agents.analysts.news_analyst import NewsAnalyst
from agents.analysts.social_media_analyst import SocialMediaAnalyst
from agents.researchers.bull_researcher import BullResearcher
from agents.researchers.bear_researcher import BearResearcher
from agents.managers.research_manager import ResearchManager
from agents.managers.risk_manager import RiskManager
from agents.trader.trader import Trader

logger = get_logger(__name__)


class CryptoAgentSystem:
    """加密货币多智能体专家系统"""
    
    def __init__(self):
        self.analysts = [
            MarketAnalyst("Market Analyst"),
            FundamentalsAnalyst("Fundamentals Analyst"),
            NewsAnalyst("News Analyst"),
            SocialMediaAnalyst("Social Media Analyst")
        ]
        
        self.researchers = [
            BullResearcher("Bull Researcher"),
            BearResearcher("Bear Researcher")
        ]
        
        self.managers = [
            ResearchManager("Research Manager")
        ]
        
        self.trader = Trader("Trader")
        self.risk_manager = RiskManager("Risk Manager")
    
    def run_analysis(self, symbol: str) -> Dict[str, Any]:
        """运行完整的分析流程"""
        try:
            logger.info(f"开始分析 {symbol}")
            
            # 创建初始状态
            state = AgentState(symbol)
            
            # 阶段1：分析师团队并行分析
            logger.info("=== 阶段1：分析师团队分析 ===")
            for analyst in self.analysts:
                try:
                    logger.info(f"执行 {analyst.name} 分析")
                    state = analyst.process(state)
                except Exception as e:
                    logger.error(f"{analyst.name} 分析失败: {e}")
            
            # 阶段2：研究员辩论
            logger.info("=== 阶段2：研究员辩论 ===")
            for researcher in self.researchers:
                try:
                    logger.info(f"执行 {researcher.name} 分析")
                    state = researcher.process(state)
                except Exception as e:
                    logger.error(f"{researcher.name} 分析失败: {e}")
            
            # 阶段3：交易员决策
            logger.info("=== 阶段3：交易员决策 ===")
            try:
                logger.info(f"执行 {self.trader.name} 决策")
                state = self.trader.process(state)
            except Exception as e:
                logger.error(f"{self.trader.name} 决策失败: {e}")
            
            # 阶段4：风险管理
            logger.info("=== 阶段4：风险管理 ===")
            try:
                logger.info(f"执行 {self.risk_manager.name} 风险评估")
                state = self.risk_manager.process(state)
            except Exception as e:
                logger.error(f"{self.risk_manager.name} 风险评估失败: {e}")
            
            # 阶段5：管理层决策
            logger.info("=== 阶段5：管理层决策 ===")
            for manager in self.managers:
                try:
                    logger.info(f"执行 {manager.name} 决策")
                    state = manager.process(state)
                except Exception as e:
                    logger.error(f"{manager.name} 决策失败: {e}")
            
            # 生成最终输出
            final_output = self._generate_final_output(state)
            
            # 保存结果
            self._save_results(final_output)
            
            logger.info(f"分析完成: {symbol}")
            return final_output
            
        except Exception as e:
            logger.error(f"分析流程失败: {e}")
            return {"error": str(e)}
    
    def _generate_final_output(self, state: AgentState) -> Dict[str, Any]:
        """生成最终输出"""
        try:
            # 获取交易决策
            trading_decision = state.trading_decision or {}
            final_risk_decision = state.final_risk_decision or {}
            
            # 获取研究共识
            research_consensus = state.research_consensus or {}
            manager_consensus = research_consensus.get("manager_consensus", {})
            consensus_text = manager_consensus.get("consensus", "无研究共识")
            
            # 提取交易决策信息
            decision = trading_decision.get("decision", "观望")
            entry_price = trading_decision.get("entry_price", "NA")
            stop_loss = trading_decision.get("stop_loss", "NA")
            take_profit = trading_decision.get("take_profit", "NA")
            confidence_score = trading_decision.get("confidence_score", 0.5)
            
            # 提取风险决策信息
            risk_decision = final_risk_decision.get("final_decision", "观望")
            risk_level = final_risk_decision.get("risk_level", "medium")
            position_size = final_risk_decision.get("position_size", 0.2)
            
            # 判断趋势
            if decision == "买入" or risk_decision == "买入":
                trend = "bullish"
            elif decision == "卖出" or risk_decision == "卖出":
                trend = "bearish"
            else:
                trend = "neutral"
            
            # 构建分析摘要
            analysis_reports = state.analysis_reports or {}
            analysis_summary = {
                "fundamental": analysis_reports.get("fundamental", {}).get("summary", "基于基本面分析"),
                "technical": analysis_reports.get("technical", {}).get("summary", "基于技术分析"),
                "news": analysis_reports.get("news", {}).get("summary", "基于新闻分析"),
                "social": analysis_reports.get("social", {}).get("summary", "基于社交分析")
            }
            
            # 生成最终输出
            final_output = {
                "symbol": state.symbol,
                "trend": trend,
                "entry_price": entry_price,
                "stop_loss": stop_loss,
                "take_profit": take_profit,
                "confidence_score": confidence_score,
                "risk_level": risk_level,
                "position_size": position_size,
                "analysis_summary": analysis_summary,
                "research_consensus": consensus_text,
                "trading_decision": trading_decision.get("analysis", ""),
                "risk_decision": final_risk_decision.get("analysis", ""),
                "timestamp": str(pd.Timestamp.now())
            }
            
            return final_output
            
        except Exception as e:
            logger.error(f"生成最终输出失败: {e}")
            return {"error": f"生成输出失败: {str(e)}"}
    
    def _save_results(self, results: Dict[str, Any]):
        """保存结果到文件"""
        try:
            # 确保输出目录存在
            output_dir = "output"
            if not os.path.exists(output_dir):
                os.makedirs(output_dir)
            
            # 保存到JSON文件
            output_file = os.path.join(output_dir, "results.json")
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(results, f, ensure_ascii=False, indent=2)
            
            logger.info(f"结果已保存到: {output_file}")
            
        except Exception as e:
            logger.error(f"保存结果失败: {e}")


def main():
    """主函数"""
    try:
        # 验证配置
        if not Config.validate_config():
            print("❌ 配置验证失败，请检查 .env 文件")
            return
        
        # 创建系统实例
        system = CryptoAgentSystem()
        
        # 获取用户输入
        symbol = input("请输入要分析的币种（如 BTC/USDT）: ").strip()
        
        if not symbol:
            symbol = "BTC/USDT"  # 默认值
        
        print(f"\n🚀 开始分析 {symbol}...")
        
        # 运行分析
        results = system.run_analysis(symbol)
        
        # 显示结果
        print(f"\n📊 分析结果:")
        print(f"币种: {results.get('symbol', 'Unknown')}")
        print(f"趋势: {results.get('trend', 'Unknown')}")
        print(f"置信度: {results.get('confidence_score', 0):.2f}")
        print(f"风险等级: {results.get('risk_level', 'Unknown')}")
        
        if "error" in results:
            print(f"❌ 分析失败: {results['error']}")
        else:
            print("✅ 分析完成！详细结果已保存到 output/results.json")
        
    except KeyboardInterrupt:
        print("\n⚠️ 用户中断分析")
    except Exception as e:
        logger.error(f"主程序执行失败: {e}")
        print(f"❌ 程序执行失败: {e}")


if __name__ == "__main__":
    main() 