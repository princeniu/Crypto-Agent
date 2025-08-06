"""
社交数据提供模块
获取Reddit等社交媒体情绪数据
"""

import requests
import time
from typing import Dict, Any, List, Optional
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class SocialDataProvider:
    """社交数据提供类"""
    
    def __init__(self):
        self.reddit_base_url = "https://www.reddit.com"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Crypto-Agent/1.0 (by /u/crypto_agent_bot)'
        })
    
    def get_reddit_posts(self, subreddit: str, coin_symbol: str, limit: int = 20) -> List[Dict[str, Any]]:
        """获取Reddit帖子"""
        try:
            url = f"{self.reddit_base_url}/r/{subreddit}/search.json"
            params = {
                'q': coin_symbol,
                'restrict_sr': 'true',
                'sort': 'hot',
                't': 'day',
                'limit': limit
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                posts = data.get('data', {}).get('children', [])
                
                reddit_posts = []
                for post in posts:
                    post_data = post.get('data', {})
                    reddit_post = {
                        'id': post_data.get('id'),
                        'title': post_data.get('title'),
                        'url': f"https://reddit.com{post_data.get('permalink', '')}",
                        'score': post_data.get('score', 0),
                        'upvote_ratio': post_data.get('upvote_ratio', 0),
                        'num_comments': post_data.get('num_comments', 0),
                        'created_utc': post_data.get('created_utc'),
                        'subreddit': post_data.get('subreddit'),
                        'author': post_data.get('author'),
                        'selftext': post_data.get('selftext', '')[:500]  # 限制长度
                    }
                    reddit_posts.append(reddit_post)
                
                logger.info(f"成功获取 r/{subreddit} 中 {coin_symbol} 相关帖子 {len(reddit_posts)} 条")
                return reddit_posts
            else:
                logger.error(f"获取Reddit帖子失败: {response.status_code}")
                return []
                
        except Exception as e:
            logger.error(f"获取Reddit帖子异常: {e}")
            return []
    
    def get_crypto_subreddits_posts(self, coin_symbol: str) -> List[Dict[str, Any]]:
        """获取多个加密货币相关subreddit的帖子"""
        crypto_subreddits = [
            'cryptocurrency',
            'bitcoin',
            'cryptomarkets',
            'altcoin',
            'cryptotrading'
        ]
        
        all_posts = []
        for subreddit in crypto_subreddits:
            try:
                posts = self.get_reddit_posts(subreddit, coin_symbol, limit=10)
                all_posts.extend(posts)
                time.sleep(1)  # 避免请求过快
            except Exception as e:
                logger.error(f"获取 r/{subreddit} 帖子失败: {e}")
                continue
        
        return all_posts
    
    def analyze_social_sentiment(self, posts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """分析社交媒体情绪"""
        try:
            if not posts:
                return {
                    'sentiment_score': 0,
                    'positive_count': 0,
                    'negative_count': 0,
                    'neutral_count': 0,
                    'total_count': 0,
                    'avg_score': 0,
                    'avg_upvote_ratio': 0
                }
            
            positive_keywords = [
                'bullish', 'moon', 'pump', 'buy', 'hodl', 'diamond hands', 'to the moon',
                'surge', 'rally', 'breakout', 'accumulate', 'strong', 'bull run',
                '看涨', '牛市', '买入', '持有', '突破', '强势', '上涨'
            ]
            
            negative_keywords = [
                'bearish', 'dump', 'sell', 'crash', 'bear market', 'paper hands',
                'dump', 'sell-off', 'correction', 'weak', 'bear run', 'short',
                '看跌', '熊市', '卖出', '崩盘', '抛售', '弱势', '下跌'
            ]
            
            positive_count = 0
            negative_count = 0
            neutral_count = 0
            total_score = 0
            total_upvote_ratio = 0
            
            for post in posts:
                title = post.get('title', '').lower()
                selftext = post.get('selftext', '').lower()
                content = f"{title} {selftext}"
                
                # 检查正面关键词
                if any(keyword in content for keyword in positive_keywords):
                    positive_count += 1
                # 检查负面关键词
                elif any(keyword in content for keyword in negative_keywords):
                    negative_count += 1
                else:
                    neutral_count += 1
                
                total_score += post.get('score', 0)
                total_upvote_ratio += post.get('upvote_ratio', 0)
            
            total_count = len(posts)
            
            # 计算情绪得分 (-1 到 1)
            if total_count > 0:
                sentiment_score = (positive_count - negative_count) / total_count
                avg_score = total_score / total_count
                avg_upvote_ratio = total_upvote_ratio / total_count
            else:
                sentiment_score = 0
                avg_score = 0
                avg_upvote_ratio = 0
            
            return {
                'sentiment_score': sentiment_score,
                'positive_count': positive_count,
                'negative_count': negative_count,
                'neutral_count': neutral_count,
                'total_count': total_count,
                'avg_score': avg_score,
                'avg_upvote_ratio': avg_upvote_ratio
            }
            
        except Exception as e:
            logger.error(f"分析社交情绪失败: {e}")
            return {
                'sentiment_score': 0,
                'positive_count': 0,
                'negative_count': 0,
                'neutral_count': 0,
                'total_count': 0,
                'avg_score': 0,
                'avg_upvote_ratio': 0
            }
    
    def get_social_data(self, coin_symbol: str) -> Dict[str, Any]:
        """获取完整的社交数据"""
        try:
            # 获取Reddit帖子
            reddit_posts = self.get_crypto_subreddits_posts(coin_symbol)
            
            # 分析社交情绪
            sentiment_analysis = self.analyze_social_sentiment(reddit_posts)
            
            # 计算热度指标
            total_score = sum(post.get('score', 0) for post in reddit_posts)
            total_comments = sum(post.get('num_comments', 0) for post in reddit_posts)
            
            # 合并数据
            social_data = {
                'symbol': coin_symbol,
                'reddit_posts': reddit_posts,
                'sentiment_analysis': sentiment_analysis,
                'analysis_summary': {
                    'total_posts': len(reddit_posts),
                    'total_score': total_score,
                    'total_comments': total_comments,
                    'sentiment_score': sentiment_analysis.get('sentiment_score', 0),
                    'avg_score': sentiment_analysis.get('avg_score', 0),
                    'avg_upvote_ratio': sentiment_analysis.get('avg_upvote_ratio', 0),
                    'engagement_rate': total_comments / len(reddit_posts) if reddit_posts else 0
                }
            }
            
            logger.info(f"成功获取 {coin_symbol} 社交数据")
            return social_data
            
        except Exception as e:
            logger.error(f"获取社交数据失败: {e}")
            return {}


if __name__ == "__main__":
    # 独立测试
    provider = SocialDataProvider()
    
    # 测试获取BTC社交数据
    symbol = "BTC"
    social_data = provider.get_social_data(symbol)
    
    print(f"=== {symbol} 社交数据测试 ===")
    if social_data:
        analysis = social_data.get('analysis_summary', {})
        
        print(f"Reddit帖子数量: {analysis.get('total_posts', 0)}")
        print(f"总评分: {analysis.get('total_score', 0)}")
        print(f"总评论数: {analysis.get('total_comments', 0)}")
        print(f"情绪得分: {analysis.get('sentiment_score', 0):.3f}")
        print(f"平均评分: {analysis.get('avg_score', 0):.2f}")
        print(f"平均点赞率: {analysis.get('avg_upvote_ratio', 0):.3f}")
        print(f"参与度: {analysis.get('engagement_rate', 0):.2f}")
        
        # 显示前几条帖子标题
        reddit_posts = social_data.get('reddit_posts', [])
        if reddit_posts:
            print(f"\n前3条Reddit帖子:")
            for i, post in enumerate(reddit_posts[:3]):
                print(f"{i+1}. {post.get('title', 'No title')} (评分: {post.get('score', 0)})")
    else:
        print("获取社交数据失败") 