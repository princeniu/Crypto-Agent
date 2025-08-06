"""
配置管理模块
包含API密钥、环境配置等
"""

import os
from typing import Optional
from dotenv import load_dotenv

# 加载环境变量
load_dotenv()


class Config:
    """配置管理类"""
    
    # OpenAI配置
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY", "")
    OPENAI_MODEL = os.getenv("OPENAI_MODEL", "gpt-4o-mini")
    OPENAI_TEMPERATURE = float(os.getenv("OPENAI_TEMPERATURE", "0.1"))
    
    # 交易所配置
    EXCHANGE_NAME = os.getenv("EXCHANGE_NAME", "binance")
    EXCHANGE_API_KEY = os.getenv("EXCHANGE_API_KEY", "")
    EXCHANGE_SECRET = os.getenv("EXCHANGE_SECRET", "")
    
    # 数据API配置
    COINGECKO_API_KEY = os.getenv("COINGECKO_API_KEY", "")
    CRYPTOPANIC_API_KEY = os.getenv("CRYPTOPANIC_API_KEY", "")
    TWITTER_API_KEY = os.getenv("TWITTER_API_KEY", "")
    TWITTER_API_SECRET = os.getenv("TWITTER_API_SECRET", "")
    
    # 输出配置
    OUTPUT_DIR = os.getenv("OUTPUT_DIR", "output")
    LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")
    
    # 分析配置
    DEFAULT_TIMEFRAME = os.getenv("DEFAULT_TIMEFRAME", "1h")
    DEFAULT_LIMIT = int(os.getenv("DEFAULT_LIMIT", "100"))
    
    @classmethod
    def validate_config(cls) -> bool:
        """验证配置是否完整"""
        required_keys = [
            "OPENAI_API_KEY"
        ]
        
        missing_keys = []
        for key in required_keys:
            if not getattr(cls, key):
                missing_keys.append(key)
        
        if missing_keys:
            print(f"⚠️ 缺少必需的配置项: {missing_keys}")
            print("请在 .env 文件中设置这些配置项")
            return False
        
        return True
    
    @classmethod
    def get_exchange_config(cls) -> dict:
        """获取交易所配置"""
        config = {
            "exchange": cls.EXCHANGE_NAME
        }
        
        if cls.EXCHANGE_API_KEY and cls.EXCHANGE_SECRET:
            config.update({
                "apiKey": cls.EXCHANGE_API_KEY,
                "secret": cls.EXCHANGE_SECRET
            })
        
        return config


if __name__ == "__main__":
    # 独立测试
    print("配置验证测试:")
    print(f"OpenAI Model: {Config.OPENAI_MODEL}")
    print(f"Exchange: {Config.EXCHANGE_NAME}")
    print(f"Output Dir: {Config.OUTPUT_DIR}")
    
    is_valid = Config.validate_config()
    print(f"配置验证结果: {'✅ 通过' if is_valid else '❌ 失败'}")
    
    exchange_config = Config.get_exchange_config()
    print(f"交易所配置: {exchange_config}") 