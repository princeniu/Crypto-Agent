"""
基本面数据提供模块
获取CoinGecko等链上数据和基本面信息
"""

import requests
import time
from typing import Dict, Any, Optional
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class FundamentalsDataProvider:
    """基本面数据提供类"""
    
    def __init__(self):
        self.coingecko_base_url = "https://api.coingecko.com/api/v3"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Crypto-Agent/1.0'
        })
    
    def get_coin_info(self, coin_id: str) -> Dict[str, Any]:
        """获取币种基本信息"""
        try:
            url = f"{self.coingecko_base_url}/coins/{coin_id}"
            response = self.session.get(url)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'id': data.get('id'),
                    'name': data.get('name'),
                    'symbol': data.get('symbol', '').upper(),
                    'market_cap': data.get('market_data', {}).get('market_cap', {}).get('usd', 0),
                    'market_cap_rank': data.get('market_cap_rank'),
                    'total_volume': data.get('market_data', {}).get('total_volume', {}).get('usd', 0),
                    'circulating_supply': data.get('market_data', {}).get('circulating_supply', 0),
                    'total_supply': data.get('market_data', {}).get('total_supply', 0),
                    'max_supply': data.get('market_data', {}).get('max_supply', 0),
                    'ath': data.get('market_data', {}).get('ath', {}).get('usd', 0),
                    'ath_change_percentage': data.get('market_data', {}).get('ath_change_percentage', {}).get('usd', 0),
                    'atl': data.get('market_data', {}).get('atl', {}).get('usd', 0),
                    'atl_change_percentage': data.get('market_data', {}).get('atl_change_percentage', {}).get('usd', 0),
                    'price_change_24h': data.get('market_data', {}).get('price_change_percentage_24h', 0),
                    'price_change_7d': data.get('market_data', {}).get('price_change_percentage_7d', 0),
                    'price_change_30d': data.get('market_data', {}).get('price_change_percentage_30d', 0),
                    'community_score': data.get('community_score', 0),
                    'developer_score': data.get('developer_score', 0),
                    'liquidity_score': data.get('liquidity_score', 0),
                    'public_interest_score': data.get('public_interest_score', 0),
                    'trust_score': data.get('trust_score', 0),
                    'description': data.get('description', {}).get('en', ''),
                    'categories': data.get('categories', []),
                    'links': data.get('links', {})
                }
            else:
                logger.error(f"获取币种信息失败: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"获取币种信息异常: {e}")
            return {}
    
    def get_market_data(self, coin_id: str) -> Dict[str, Any]:
        """获取市场数据"""
        try:
            url = f"{self.coingecko_base_url}/coins/{coin_id}/market_chart"
            params = {
                'vs_currency': 'usd',
                'days': '30'
            }
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    'prices': data.get('prices', []),
                    'market_caps': data.get('market_caps', []),
                    'total_volumes': data.get('total_volumes', [])
                }
            else:
                logger.error(f"获取市场数据失败: {response.status_code}")
                return {}
                
        except Exception as e:
            logger.error(f"获取市场数据异常: {e}")
            return {}
    
    def search_coin_id(self, symbol: str) -> Optional[str]:
        """搜索币种ID"""
        try:
            url = f"{self.coingecko_base_url}/search"
            params = {'query': symbol}
            
            response = self.session.get(url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                coins = data.get('coins', [])
                
                if coins:
                    # 返回第一个匹配的币种ID
                    return coins[0].get('id')
            
            return None
            
        except Exception as e:
            logger.error(f"搜索币种ID异常: {e}")
            return None
    
    def get_fundamentals_data(self, symbol: str) -> Dict[str, Any]:
        """获取完整的基本面数据"""
        try:
            # 搜索币种ID
            coin_id = self.search_coin_id(symbol)
            
            if not coin_id:
                logger.error(f"未找到币种 {symbol} 的ID")
                return {}
            
            # 获取币种信息
            coin_info = self.get_coin_info(coin_id)
            
            if not coin_info:
                return {}
            
            # 获取市场数据
            market_data = self.get_market_data(coin_id)
            
            # 合并数据
            fundamentals_data = {
                'symbol': symbol,
                'coin_info': coin_info,
                'market_data': market_data,
                'analysis_summary': {
                    'market_cap_rank': coin_info.get('market_cap_rank', 'N/A'),
                    'market_cap': coin_info.get('market_cap', 0),
                    'volume_24h': coin_info.get('total_volume', 0),
                    'circulating_supply': coin_info.get('circulating_supply', 0),
                    'price_change_24h': coin_info.get('price_change_24h', 0),
                    'community_score': coin_info.get('community_score', 0),
                    'developer_score': coin_info.get('developer_score', 0),
                    'trust_score': coin_info.get('trust_score', 0)
                }
            }
            
            logger.info(f"成功获取 {symbol} 基本面数据")
            return fundamentals_data
            
        except Exception as e:
            logger.error(f"获取基本面数据失败: {e}")
            return {}


if __name__ == "__main__":
    # 独立测试
    provider = FundamentalsDataProvider()
    
    # 测试获取BTC基本面数据
    symbol = "BTC"
    fundamentals_data = provider.get_fundamentals_data(symbol)
    
    print(f"=== {symbol} 基本面数据测试 ===")
    if fundamentals_data:
        coin_info = fundamentals_data.get('coin_info', {})
        analysis = fundamentals_data.get('analysis_summary', {})
        
        print(f"币种名称: {coin_info.get('name', 'Unknown')}")
        print(f"市值排名: {analysis.get('market_cap_rank', 'N/A')}")
        print(f"市值: ${analysis.get('market_cap', 0):,.0f}")
        print(f"24小时成交量: ${analysis.get('volume_24h', 0):,.0f}")
        print(f"24小时涨跌幅: {analysis.get('price_change_24h', 0):.2f}%")
        print(f"社区评分: {analysis.get('community_score', 0)}")
        print(f"开发者评分: {analysis.get('developer_score', 0)}")
        print(f"信任评分: {analysis.get('trust_score', 0)}")
    else:
        print("获取基本面数据失败") 