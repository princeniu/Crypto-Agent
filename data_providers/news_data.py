"""
新闻数据提供模块
获取CryptoPanic等新闻数据
"""

import requests
import time
from typing import Dict, Any, List, Optional
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class NewsDataProvider:
    """新闻数据提供类"""
    
    def __init__(self):
        self.cryptopanic_base_url = "https://cryptopanic.com/api/v1"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Crypto-Agent/1.0'
        })
    
    def get_news_by_coin(self, coin_symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        """获取特定币种的新闻"""
        try:
            url = f"{self.cryptopanic_base_url}/posts/"
            params = {
                'currencies': coin_symbol,
                'filter': 'hot',
                'public': 'true',
                'limit': limit
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('results', [])
                
                news_list = []
                for post in posts:
                    news_item = {
                        'id': post.get('id'),
                        'title': post.get('title'),
                        'url': post.get('url'),
                        'published_at': post.get('published_at'),
                        'currencies': [curr.get('code') for curr in post.get('currencies', [])],
                        'source': post.get('source', {}).get('title', 'Unknown'),
                        'votes': post.get('votes', {}),
                        'metadata': post.get('metadata', {})
                    }
                    news_list.append(news_item)
                
                logger.info(f"成功获取 {coin_symbol} 相关新闻 {len(news_list)} 条")
                return news_list
            else:
                logger.error(f"获取新闻失败: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"获取新闻异常: {e}")
            return []
    
    def get_general_crypto_news(self, limit: int = 20) -> List[Dict[str, Any]]:
        """获取一般加密货币新闻"""
        try:
            url = f"{self.cryptopanic_base_url}/posts/"
            params = {
                'filter': 'hot',
                'public': 'true',
                'limit': limit
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('results', [])
                
                news_list = []
                for post in posts:
                    news_item = {
                        'id': post.get('id'),
                        'title': post.get('title'),
                        'url': post.get('url'),
                        'published_at': post.get('published_at'),
                        'currencies': [curr.get('code') for curr in post.get('currencies', [])],
                        'source': post.get('source', {}).get('title', 'Unknown'),
                        'votes': post.get('votes', {}),
                        'metadata': post.get('metadata', {})
                    }
                    news_list.append(news_item)
                
                logger.info(f"成功获取一般加密货币新闻 {len(news_list)} 条")
                return news_list
            else:
                logger.error(f"获取一般新闻失败: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"获取一般新闻异常: {e}")
            return []
    
    def analyze_news_sentiment(self, news_list: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析新闻情绪"""
        try:
            if not news_list:
                return {
                    'sentiment_score': 0,
                    'positive_count': 0,
                    'negative_count': 0,
                    'neutral_count': 0,
                    'total_count': 0
                }
            
            positive_keywords = [
                'bullish', 'surge', 'rally', 'gain', 'up', 'positive', 'growth',
                'adoption', 'partnership', 'launch', 'upgrade', 'innovation',
                '利好', '上涨', '突破', '增长', '合作', '升级', '创新'
            ]
            
            negative_keywords = [
                'bearish', 'crash', 'drop', 'fall', 'down', 'negative', 'decline',
                'hack', 'scam', 'ban', 'regulation', 'sell-off', 'dump',
                '利空', '下跌', '崩盘', '黑客', '诈骗', '禁令', '抛售'
            ]
            
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            
            for news in news_list:
                title = news.get('title', '').lower()
                
                # 检查正面关键词
                if any(keyword in title for keyword in positive_keywords):
                    positive_count += 1
                # 检查负面关键词
                elif any(keyword in title for keyword in negative_keywords):
                    negative_count += 1
                else:
                    neutral_count += 1
            
            total_count = len(news_list)
            
            # 计算情绪得分 (-1 到 1)
            if total_count > 0:
                sentiment_score = (positive_count - negative_count) / total_count
            else:
                sentiment_score = 0
            
            return {
                'sentiment_score': sentiment_score,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'neutral_count': neutral_count,
                'total_count': total_count
            }
            
        except Exception as e:
            logger.error(f"分析新闻情绪失败: {e}")
            return {
                'sentiment_score': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_count': 0
            }
    
    def get_news_data(self, coin_symbol: str) -> Dict[str, Any]:
        """获取完整的新闻数据"""
        try:
            # 获取币种相关新闻
            coin_news = self.get_news_by_coin(coin_symbol, limit=15)
            
            # 获取一般加密货币新闻
            general_news = self.get_general_crypto_news(limit=10)
            
            # 分析币种新闻情绪
            coin_sentiment = self.analyze_news_sentiment(coin_news)
            
            # 分析一般新闻情绪
            general_sentiment = self.analyze_news_sentiment(general_news)
            
            # 合并数据
            news_data = {
                'symbol': coin_symbol,
                'coin_news': coin_news,
                'general_news': general_news,
                'coin_sentiment': coin_sentiment,
                'general_sentiment': general_sentiment,
                'analysis_summary': {
                    'total_coin_news': len(coin_news),
                    'total_general_news': len(general_news),
                    'coin_sentiment_score': coin_sentiment.get('sentiment_score', 0),
                    'general_sentiment_score': general_sentiment.get('sentiment_score', 0),
                    'overall_sentiment': (coin_sentiment.get('sentiment_score', 0) + 
                                        general_sentiment.get('sentiment_score', 0)) / 2
                }
            }
            
            logger.info(f"成功获取 {coin_symbol} 新闻数据")
            return news_data
            
        except Exception as e:
            logger.error(f"获取新闻数据失败: {e}")
            return {}


if __name__ == "__main__":
    # 独立测试
    provider = NewsDataProvider()
    
    # 测试获取BTC新闻数据
    symbol = "BTC"
    news_data = provider.get_news_data(symbol)
    
    print(f"=== {symbol} 新闻数据测试 ===")
    if news_data:
        analysis = news_data.get('analysis_summary', {})
        
        print(f"币种相关新闻数量: {analysis.get('total_coin_news', 0)}")
        print(f"一般新闻数量: {analysis.get('total_general_news', 0)}")
        print(f"币种新闻情绪得分: {analysis.get('coin_sentiment_score', 0):.3f}")
        print(f"一般新闻情绪得分: {analysis.get('general_sentiment_score', 0):.3f}")
        print(f"整体情绪得分: {analysis.get('overall_sentiment', 0):.3f}")
        
        # 显示前几条新闻标题
        coin_news = news_data.get('coin_news', [])
        if coin_news:
            print(f"\n前3条币种相关新闻:")
            for i, news in enumerate(coin_news[:3]):
                print(f"{i+1}. {news.get('title', 'No title')}")
    else:
        print("获取新闻数据失败") 