"""配置管理模块"""

import os
from typing import Optional

class Config:
    """配置类"""
    
    def __init__(self):
        self.api_key: Optional[str] = os.getenv("MOWEN_API_KEY")
        self.base_url: str = os.getenv("MOWEN_BASE_URL", "https://open.mowen.cn")
        
    def validate(self) -> bool:
        """验证配置是否有效"""
        return self.api_key is not None and len(self.api_key.strip()) > 0
    
    def get_error_message(self) -> str:
        """获取配置错误信息"""
        if not self.api_key:
            return "未设置MOWEN_API_KEY环境变量，请先获取墨问API密钥并设置环境变量"
        return "配置验证失败" 