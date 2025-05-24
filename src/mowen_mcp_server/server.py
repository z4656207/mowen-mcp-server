"""
墨问 API MCP 服务器主文件（修复版）

这个服务器封装了墨问笔记软件的API，提供以下功能：
1. 创建笔记
2. 编辑笔记  
3. 设置笔记权限
4. 重置API密钥
"""

import asyncio
import json
import logging
import os
from typing import Any, Dict, List, Optional
from urllib.parse import urljoin
import nest_asyncio

import httpx
from mcp.server.fastmcp import FastMCP

# 允许嵌套事件循环
nest_asyncio.apply()

# 配置日志
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("mowen-mcp-server")

# 创建FastMCP服务器实例
mcp = FastMCP("墨问笔记MCP服务器")

class MowenAPI:
    """墨问API客户端类，封装所有API调用"""
    
    def __init__(self, api_key: str, base_url: str = "https://open.mowen.cn"):
        self.api_key = api_key
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }
    
    async def create_note(self, body: Dict[str, Any], settings: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        创建笔记
        
        参数:
        - body: 笔记内容（NoteAtom结构）
        - settings: 笔记设置（可选）
        """
        url = urljoin(self.base_url, "/api/open/api/v1/note/create")
        payload = {"body": body}
        if settings:
            payload["settings"] = settings
            
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
    
    async def edit_note(self, note_id: str, body: Dict[str, Any]) -> Dict[str, Any]:
        """
        编辑笔记
        
        参数:
        - note_id: 笔记ID
        - body: 新的笔记内容（NoteAtom结构）
        """
        url = urljoin(self.base_url, "/api/open/api/v1/note/edit")
        payload = {
            "noteId": note_id,
            "body": body
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
    
    async def set_note_privacy(self, note_id: str, privacy_type: str, rule: Optional[Dict[str, Any]] = None) -> Dict[str, Any]:
        """
        设置笔记隐私
        
        参数:
        - note_id: 笔记ID
        - privacy_type: 隐私类型 (public/private/rule)
        - rule: 隐私规则（可选）
        """
        url = urljoin(self.base_url, "/api/open/api/v1/note/set")
        privacy_settings = {"type": privacy_type}
        if rule:
            privacy_settings["rule"] = rule
            
        payload = {
            "noteId": note_id,
            "section": 1,  # 1表示笔记隐私设置
            "settings": {
                "privacy": privacy_settings
            }
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
    
    async def reset_api_key(self) -> Dict[str, Any]:
        """重置API密钥"""
        url = urljoin(self.base_url, "/api/open/api/v1/auth/key/reset")
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json={})
            response.raise_for_status()
            return response.json()

class NoteAtomBuilder:
    """NoteAtom结构构建器，帮助构建符合墨问格式的笔记内容"""
    
    @staticmethod
    def create_doc(paragraphs: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建文档根节点"""
        return {
            "type": "doc",
            "content": paragraphs
        }
    
    @staticmethod
    def create_paragraph(texts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建段落节点"""
        if not texts:
            return {"type": "paragraph"}
        return {
            "type": "paragraph", 
            "content": texts
        }
    
    @staticmethod
    def create_text(text: str, marks: Optional[List[Dict[str, Any]]] = None) -> Dict[str, Any]:
        """创建文本节点"""
        node = {
            "type": "text",
            "text": text
        }
        if marks:
            node["marks"] = marks
        return node
    
    @staticmethod
    def create_bold_mark() -> Dict[str, Any]:
        """创建加粗标记"""
        return {"type": "bold"}
    
    @staticmethod  
    def create_highlight_mark() -> Dict[str, Any]:
        """创建高亮标记"""
        return {"type": "highlight"}
    
    @staticmethod
    def create_link_mark(href: str) -> Dict[str, Any]:
        """创建链接标记"""
        return {
            "type": "link",
            "attrs": {"href": href}
        }

# 全局API客户端变量
mowen_api: Optional[MowenAPI] = None

def run_async_safely(coro):
    """安全地运行异步函数"""
    try:
        # 尝试在现有事件循环中运行
        loop = asyncio.get_event_loop()
        if loop.is_running():
            # 使用 nest_asyncio 允许嵌套
            return asyncio.run(coro)
        else:
            return loop.run_until_complete(coro)
    except RuntimeError:
        # 没有事件循环，创建新的
        return asyncio.run(coro)

@mcp.tool()
def create_note(content: str, auto_publish: bool = False, tags: List[str] = None) -> str:
    """创建一篇新的墨问笔记"""
    if mowen_api is None:
        return "错误：未设置API密钥。请先设置MOWEN_API_KEY环境变量。"
    
    if tags is None:
        tags = []
    
    try:
        # 构建简单的NoteAtom结构
        paragraph = NoteAtomBuilder.create_paragraph([
            NoteAtomBuilder.create_text(content)
        ])
        body = NoteAtomBuilder.create_doc([paragraph])
        
        settings = {
            "autoPublish": auto_publish,
            "tags": tags
        }
        
        # 使用修复的异步运行方式
        result = run_async_safely(mowen_api.create_note(body, settings))
            
        return f"✅ 笔记创建成功！\n\n笔记ID: {result.get('noteId', 'N/A')}\n内容: {content}\n自动发布: {auto_publish}\n标签: {', '.join(tags)}"
    except httpx.HTTPStatusError as e:
        error_detail = ""
        try:
            error_json = e.response.json()
            error_detail = f"\n错误代码: {error_json.get('code', 'N/A')}\n错误原因: {error_json.get('reason', 'N/A')}\n错误信息: {error_json.get('message', 'N/A')}"
        except:
            error_detail = f"\nHTTP状态码: {e.response.status_code}"
            
        return f"❌ API调用失败: {str(e)}{error_detail}"
    except Exception as e:
        return f"❌ 发生错误: {str(e)}"

@mcp.tool()
def create_rich_note(paragraphs: List[Dict[str, Any]], auto_publish: bool = False, tags: List[str] = None) -> str:
    """创建富文本笔记，支持段落格式、加粗、高亮、链接等"""
    if mowen_api is None:
        return "错误：未设置API密钥。请先设置MOWEN_API_KEY环境变量。"
    
    if tags is None:
        tags = []
    
    try:
        paragraphs_built = []
        for para_data in paragraphs:
            texts = []
            for text_data in para_data["texts"]:
                marks = []
                if text_data.get("bold"):
                    marks.append(NoteAtomBuilder.create_bold_mark())
                if text_data.get("highlight"):
                    marks.append(NoteAtomBuilder.create_highlight_mark())
                if text_data.get("link"):
                    marks.append(NoteAtomBuilder.create_link_mark(text_data["link"]))
                
                text_node = NoteAtomBuilder.create_text(
                    text_data["text"], 
                    marks if marks else None
                )
                texts.append(text_node)
            
            paragraphs_built.append(NoteAtomBuilder.create_paragraph(texts))
        
        body = NoteAtomBuilder.create_doc(paragraphs_built)
        settings = {
            "autoPublish": auto_publish,
            "tags": tags
        }
        
        # 使用修复的异步运行方式
        result = run_async_safely(mowen_api.create_note(body, settings))
            
        return f"✅ 富文本笔记创建成功！\n\n笔记ID: {result.get('noteId', 'N/A')}\n段落数: {len(paragraphs_built)}\n自动发布: {auto_publish}\n标签: {', '.join(tags)}"
    except httpx.HTTPStatusError as e:
        error_detail = ""
        try:
            error_json = e.response.json()
            error_detail = f"\n错误代码: {error_json.get('code', 'N/A')}\n错误原因: {error_json.get('reason', 'N/A')}\n错误信息: {error_json.get('message', 'N/A')}"
        except:
            error_detail = f"\nHTTP状态码: {e.response.status_code}"
            
        return f"❌ API调用失败: {str(e)}{error_detail}"
    except Exception as e:
        return f"❌ 发生错误: {str(e)}"

@mcp.tool()
def edit_note(note_id: str, content: str) -> str:
    """编辑已存在的笔记内容"""
    if mowen_api is None:
        return "错误：未设置API密钥。请先设置MOWEN_API_KEY环境变量。"
    
    try:
        paragraph = NoteAtomBuilder.create_paragraph([
            NoteAtomBuilder.create_text(content)
        ])
        body = NoteAtomBuilder.create_doc([paragraph])
        
        # 使用修复的异步运行方式
        result = run_async_safely(mowen_api.edit_note(note_id, body))
            
        return f"✅ 笔记编辑成功！\n\n笔记ID: {result.get('noteId', note_id)}\n新内容: {content}"
    except httpx.HTTPStatusError as e:
        error_detail = ""
        try:
            error_json = e.response.json()
            error_detail = f"\n错误代码: {error_json.get('code', 'N/A')}\n错误原因: {error_json.get('reason', 'N/A')}\n错误信息: {error_json.get('message', 'N/A')}"
        except:
            error_detail = f"\nHTTP状态码: {e.response.status_code}"
            
        return f"❌ API调用失败: {str(e)}{error_detail}"
    except Exception as e:
        return f"❌ 发生错误: {str(e)}"

@mcp.tool()
def set_note_privacy(note_id: str, privacy_type: str, no_share: bool = False, expire_at: int = 0) -> str:
    """设置笔记的隐私权限
    
    参数:
    - note_id: 笔记ID
    - privacy_type: 隐私类型 ('public' - 完全公开, 'private' - 私有, 'rule' - 规则公开)
    - no_share: 当privacy_type为'rule'时，是否禁止分享
    - expire_at: 当privacy_type为'rule'时，过期时间戳（0表示永不过期）
    """
    if mowen_api is None:
        return "错误：未设置API密钥。请先设置MOWEN_API_KEY环境变量。"
    
    try:
        rule = None
        if privacy_type == "rule":
            rule = {
                "noShare": no_share,
                "expireAt": str(expire_at)
            }
        
        # 使用修复的异步运行方式
        result = run_async_safely(mowen_api.set_note_privacy(note_id, privacy_type, rule))
        
        privacy_desc = {
            "public": "完全公开",
            "private": "私有",
            "rule": "规则公开"
        }
        
        response_text = f"✅ 笔记隐私设置成功！\n\n笔记ID: {note_id}\n隐私类型: {privacy_desc.get(privacy_type, privacy_type)}"
        
        if rule:
            response_text += f"\n禁止分享: {'是' if rule['noShare'] else '否'}"
            expire_time = rule['expireAt']
            if expire_time == "0":
                response_text += "\n有效期: 永久"
            else:
                response_text += f"\n过期时间戳: {expire_time}"
                
        return response_text
    except httpx.HTTPStatusError as e:
        error_detail = ""
        try:
            error_json = e.response.json()
            error_detail = f"\n错误代码: {error_json.get('code', 'N/A')}\n错误原因: {error_json.get('reason', 'N/A')}\n错误信息: {error_json.get('message', 'N/A')}"
        except:
            error_detail = f"\nHTTP状态码: {e.response.status_code}"
            
        return f"❌ API调用失败: {str(e)}{error_detail}"
    except Exception as e:
        return f"❌ 发生错误: {str(e)}"

@mcp.tool()
def reset_api_key() -> str:
    """重置墨问API密钥（注意：会使当前密钥失效）"""
    if mowen_api is None:
        return "错误：未设置API密钥。请先设置MOWEN_API_KEY环境变量。"
    
    try:
        # 使用修复的异步运行方式
        result = run_async_safely(mowen_api.reset_api_key())
            
        new_api_key = result.get("apiKey", "N/A")
        
        return f"⚠️ API密钥重置成功！\n\n新的API密钥: {new_api_key}\n\n重要提醒：\n1. 请立即保存新的API密钥\n2. 旧的API密钥已立即失效\n3. 需要更新您的应用配置"
    except httpx.HTTPStatusError as e:
        error_detail = ""
        try:
            error_json = e.response.json()
            error_detail = f"\n错误代码: {error_json.get('code', 'N/A')}\n错误原因: {error_json.get('reason', 'N/A')}\n错误信息: {error_json.get('message', 'N/A')}"
        except:
            error_detail = f"\nHTTP状态码: {e.response.status_code}"
            
        return f"❌ API调用失败: {str(e)}{error_detail}"
    except Exception as e:
        return f"❌ 发生错误: {str(e)}"

def main():
    """主函数：启动MCP服务器"""
    global mowen_api
    
    # 获取API密钥
    api_key = os.getenv("MOWEN_API_KEY")
    if not api_key:
        logger.error("未设置API密钥。请先设置MOWEN_API_KEY环境变量。")
        return
    
    # 初始化API客户端
    mowen_api = MowenAPI(api_key)
    logger.info("墨问API客户端初始化完成")
    
    # 启动服务器
    logger.info("正在启动墨问MCP服务器...")
    mcp.run()

if __name__ == "__main__":
    main() 