"""
日志工具模块
用于记录智能体运行日志和调试信息
"""

import logging
import os
from datetime import datetime
from typing import Optional
from utils.config import Config


class Logger:
    """日志管理类"""
    
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(getattr(logging, level.upper()))
        
        # 避免重复添加handler
        if not self.logger.handlers:
            self._setup_handlers()
    
    def _setup_handlers(self):
        """设置日志处理器"""
        # 控制台输出
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.INFO)
        
        # 文件输出
        log_dir = "logs"
        if not os.path.exists(log_dir):
            os.makedirs(log_dir)
        
        file_handler = logging.FileHandler(
            f"{log_dir}/crypto_agent_{datetime.now().strftime('%Y%m%d')}.log",
            encoding='utf-8'
        )
        file_handler.setLevel(logging.DEBUG)
        
        # 格式化器
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        console_handler.setFormatter(formatter)
        file_handler.setFormatter(formatter)
        
        # 添加处理器
        self.logger.addHandler(console_handler)
        self.logger.addHandler(file_handler)
    
    def info(self, message: str):
        """信息日志"""
        self.logger.info(message)
    
    def debug(self, message: str):
        """调试日志"""
        self.logger.debug(message)
    
    def warning(self, message: str):
        """警告日志"""
        self.logger.warning(message)
    
    def error(self, message: str):
        """错误日志"""
        self.logger.error(message)
    
    def critical(self, message: str):
        """严重错误日志"""
        self.logger.critical(message)


def get_logger(name: str) -> Logger:
    """获取日志实例"""
    return Logger(name, Config.LOG_LEVEL)


if __name__ == "__main__":
    # 独立测试
    logger = get_logger("test")
    
    logger.info("这是一条信息日志")
    logger.debug("这是一条调试日志")
    logger.warning("这是一条警告日志")
    logger.error("这是一条错误日志")
    
    print("日志测试完成！") 