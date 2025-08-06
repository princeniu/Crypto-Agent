"""
市场数据提供模块
使用CCXT获取K线和技术指标数据
"""

import ccxt
import pandas as pd
import numpy as np
from typing import Dict, List, Optional, Tuple
from utils.config import Config
from utils.logger import get_logger

logger = get_logger(__name__)


class MarketDataProvider:
    """市场数据提供类"""
    
    def __init__(self):
        self.exchange = None
        self._init_exchange()
    
    def _init_exchange(self):
        """初始化交易所连接"""
        try:
            exchange_config = Config.get_exchange_config()
            exchange_name = exchange_config.pop("exchange")
            
            # 创建交易所实例
            exchange_class = getattr(ccxt, exchange_name)
            self.exchange = exchange_class(exchange_config)
            
            # 加载市场信息
            self.exchange.load_markets()
            logger.info(f"成功初始化交易所: {exchange_name}")
            
        except Exception as e:
            logger.error(f"初始化交易所失败: {e}")
            # 使用公共API模式
            self.exchange = ccxt.binance()
            self.exchange.load_markets()
    
    def get_ohlcv(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> pd.DataFrame:
        """获取K线数据"""
        try:
            # 获取OHLCV数据
            ohlcv = self.exchange.fetch_ohlcv(symbol, timeframe, limit=limit)
            
            # 转换为DataFrame
            df = pd.DataFrame(ohlcv, columns=['timestamp', 'open', 'high', 'low', 'close', 'volume'])
            df['timestamp'] = pd.to_datetime(df['timestamp'], unit='ms')
            df.set_index('timestamp', inplace=True)
            
            logger.info(f"成功获取 {symbol} {timeframe} K线数据，共 {len(df)} 条")
            return df
            
        except Exception as e:
            logger.error(f"获取K线数据失败: {e}")
            return pd.DataFrame()
    
    def calculate_rsi(self, df: pd.DataFrame, period: int = 14) -> float:
        """计算RSI指标"""
        try:
            delta = df['close'].diff()
            gain = (delta.where(delta > 0, 0)).rolling(window=period).mean()
            loss = (-delta.where(delta < 0, 0)).rolling(window=period).mean()
            rs = gain / loss
            rsi = 100 - (100 / (1 + rs))
            return rsi.iloc[-1]
        except Exception as e:
            logger.error(f"计算RSI失败: {e}")
            return 50.0
    
    def calculate_macd(self, df: pd.DataFrame, fast: int = 12, slow: int = 26, signal: int = 9) -> Dict[str, float]:
        """计算MACD指标"""
        try:
            ema_fast = df['close'].ewm(span=fast).mean()
            ema_slow = df['close'].ewm(span=slow).mean()
            macd_line = ema_fast - ema_slow
            signal_line = macd_line.ewm(span=signal).mean()
            histogram = macd_line - signal_line
            
            return {
                'macd': macd_line.iloc[-1],
                'signal': signal_line.iloc[-1],
                'histogram': histogram.iloc[-1]
            }
        except Exception as e:
            logger.error(f"计算MACD失败: {e}")
            return {'macd': 0, 'signal': 0, 'histogram': 0}
    
    def calculate_bollinger_bands(self, df: pd.DataFrame, period: int = 20, std_dev: int = 2) -> Dict[str, float]:
        """计算布林带"""
        try:
            sma = df['close'].rolling(window=period).mean()
            std = df['close'].rolling(window=period).std()
            
            upper_band = sma + (std * std_dev)
            lower_band = sma - (std * std_dev)
            
            return {
                'upper': upper_band.iloc[-1],
                'middle': sma.iloc[-1],
                'lower': lower_band.iloc[-1]
            }
        except Exception as e:
            logger.error(f"计算布林带失败: {e}")
            return {'upper': 0, 'middle': 0, 'lower': 0}
    
    def get_support_resistance(self, df: pd.DataFrame) -> Dict[str, float]:
        """获取支撑阻力位"""
        try:
            high = df['high'].max()
            low = df['low'].min()
            current = df['close'].iloc[-1]
            
            # 简单的支撑阻力计算
            resistance_levels = [
                high,
                high * 0.95,
                high * 0.90
            ]
            
            support_levels = [
                low,
                low * 1.05,
                low * 1.10
            ]
            
            return {
                'resistance_levels': resistance_levels,
                'support_levels': support_levels,
                'current_price': current
            }
        except Exception as e:
            logger.error(f"计算支撑阻力位失败: {e}")
            return {'resistance_levels': [], 'support_levels': [], 'current_price': 0}
    
    def get_market_data(self, symbol: str, timeframe: str = "1h", limit: int = 100) -> Dict[str, any]:
        """获取完整的市场数据"""
        try:
            # 获取K线数据
            df = self.get_ohlcv(symbol, timeframe, limit)
            
            if df.empty:
                return {}
            
            # 计算技术指标
            rsi = self.calculate_rsi(df)
            macd = self.calculate_macd(df)
            bb = self.calculate_bollinger_bands(df)
            sr = self.get_support_resistance(df)
            
            # 计算趋势
            current_price = df['close'].iloc[-1]
            prev_price = df['close'].iloc[-2] if len(df) > 1 else current_price
            price_change = ((current_price - prev_price) / prev_price) * 100
            
            # 判断趋势
            if price_change > 1:
                trend = "bullish"
            elif price_change < -1:
                trend = "bearish"
            else:
                trend = "neutral"
            
            return {
                'symbol': symbol,
                'current_price': current_price,
                'price_change_24h': price_change,
                'volume_24h': df['volume'].iloc[-1],
                'trend': trend,
                'technical_indicators': {
                    'rsi': rsi,
                    'macd': macd,
                    'bollinger_bands': bb
                },
                'support_resistance': sr,
                'ohlcv_data': df.tail(10).to_dict('records')  # 最近10条数据
            }
            
        except Exception as e:
            logger.error(f"获取市场数据失败: {e}")
            return {}


if __name__ == "__main__":
    # 独立测试
    provider = MarketDataProvider()
    
    # 测试获取BTC/USDT数据
    symbol = "BTC/USDT"
    market_data = provider.get_market_data(symbol)
    
    print(f"=== {symbol} 市场数据测试 ===")
    if market_data:
        print(f"当前价格: {market_data.get('current_price', 0):.2f}")
        print(f"24小时涨跌幅: {market_data.get('price_change_24h', 0):.2f}%")
        print(f"趋势: {market_data.get('trend', 'unknown')}")
        print(f"RSI: {market_data.get('technical_indicators', {}).get('rsi', 0):.2f}")
        print(f"MACD: {market_data.get('technical_indicators', {}).get('macd', {})}")
    else:
        print("获取数据失败") 