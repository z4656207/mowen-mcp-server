"""
墨问 API MCP 服务器主文件

这个服务器封装了墨问笔记软件的API，提供以下功能：
1. 创建笔记（统一富文本格式）
2. 编辑笔记（统一富文本格式）
3. 设置笔记权限
4. 重置API密钥

所有笔记操作均使用统一的富文本格式，支持：
- 普通段落：文本内容和富文本格式（加粗、高亮、链接）
- 引用段落：用于创建引用文本块
- 内链笔记：用于引用其他笔记，创建笔记间的关联
"""

import asyncio
import json
import logging
import os
import mimetypes
import aiofiles
from pathlib import Path
from typing import Any, Dict, List, Optional, Literal
from urllib.parse import urljoin
import nest_asyncio

import httpx
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field

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
        
        # 记录完整的API调用参数
        import json
        logger.info(f"📤 墨问API创建笔记请求:")
        logger.info(f"URL: {url}")
        logger.info(f"Headers: {self.headers}")
        logger.info(f"Payload: {json.dumps(payload, indent=2, ensure_ascii=False)}")
            
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            logger.info(f"📥 墨问API响应状态: {response.status_code}")
            logger.info(f"📥 墨问API响应内容: {response.text}")
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
    
    async def get_upload_auth(self, file_type: int, file_name: str) -> Dict[str, Any]:
        """
        获取上传授权信息
        
        参数:
        - file_type: 文件类型 (1=图片, 2=音频, 3=PDF)
        - file_name: 文件名
        """
        url = urljoin(self.base_url, "/api/open/api/v1/upload/prepare")
        payload = {
            "fileType": file_type,
            "fileName": file_name
        }
        
        async with httpx.AsyncClient() as client:
            response = await client.post(url, headers=self.headers, json=payload)
            response.raise_for_status()
            return response.json()
    
    async def upload_file_local(self, auth_info: Dict[str, Any], file_path: str) -> Dict[str, Any]:
        """
        本地文件上传
        
        参数:
        - auth_info: 上传授权信息
        - file_path: 本地文件路径
        """
        form_info = auth_info["form"]
        endpoint = form_info["endpoint"]
        form_data = form_info
        
        # 读取文件内容
        async with aiofiles.open(file_path, 'rb') as f:
            file_content = await f.read()
        
        # 构建multipart/form-data
        files = {"file": (Path(file_path).name, file_content)}
        data = {k: v for k, v in form_data.items() if k != "file"}
        
        async with httpx.AsyncClient(timeout=300.0) as client:  # 增加超时时间
            response = await client.post(endpoint, data=data, files=files)
            response.raise_for_status()
            return response.json()
    
    async def upload_file_url(self, file_type: int, url: str, file_name: Optional[str] = None) -> Dict[str, Any]:
        """
        远程URL文件上传
        
        参数:
        - file_type: 文件类型 (1=图片, 2=音频, 3=PDF)
        - url: 文件URL
        - file_name: 文件名（可选）
        """
        api_url = urljoin(self.base_url, "/api/open/api/v1/upload/url")
        payload = {
            "fileType": file_type,
            "url": url
        }
        if file_name:
            payload["fileName"] = file_name
            
        async with httpx.AsyncClient(timeout=300.0) as client:  # 增加超时时间
            response = await client.post(api_url, headers=self.headers, json=payload)
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
    def create_quote(texts: List[Dict[str, Any]]) -> Dict[str, Any]:
        """创建引用节点"""
        if not texts:
            return {"type": "quote"}
        return {
            "type": "quote",
            "content": texts
        }
    
    @staticmethod
    def create_note(note_uuid: str) -> Dict[str, Any]:
        """创建内链笔记节点"""
        return {
            "type": "note",
            "attrs": {
                "uuid": note_uuid
            }
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
    
    @staticmethod
    def create_image(file_id: str, alt: str = "", align: str = "center") -> Dict[str, Any]:
        """创建图片节点"""
        attrs = {"uuid": file_id}
        if alt:
            attrs["alt"] = alt
        if align:
            attrs["align"] = align
        return {
            "type": "image",
            "attrs": attrs
        }
    
    @staticmethod  
    def create_audio(file_id: str, show_note: str = "") -> Dict[str, Any]:
        """创建音频节点"""
        attrs = {"audio-uuid": file_id}
        if show_note:
            attrs["show-note"] = show_note
        return {
            "type": "audio",
            "attrs": attrs
        }
    
    @staticmethod
    def create_pdf(file_id: str) -> Dict[str, Any]:
        """创建PDF节点"""
        return {
            "type": "pdf",
            "attrs": {"uuid": file_id}
        }

# 全局API客户端变量
mowen_api: Optional[MowenAPI] = None

def get_mowen_api() -> MowenAPI:
    """获取或初始化MowenAPI实例"""
    global mowen_api
    if mowen_api is None:
        api_key = os.getenv("MOWEN_API_KEY")
        if not api_key:
            raise RuntimeError("未设置API密钥。请先设置MOWEN_API_KEY环境变量。")
        mowen_api = MowenAPI(api_key)
    return mowen_api

# 文件类型映射
FILE_TYPE_MAP = {
    "image": 1,
    "audio": 2, 
    "pdf": 3
}

# 支持的文件扩展名
SUPPORTED_EXTENSIONS = {
    "image": {".gif", ".jpeg", ".jpg", ".png", ".webp"},
    "audio": {".mp3", ".mp4", ".m4a"},
    "pdf": {".pdf"}
}

# 文件大小限制 (字节)
FILE_SIZE_LIMITS = {
    "image": 50 * 1024 * 1024,  # 50MB
    "audio": 200 * 1024 * 1024,  # 200MB
    "pdf": 100 * 1024 * 1024   # 100MB
}

def get_file_type_from_extension(file_path: str) -> Optional[str]:
    """根据文件扩展名判断文件类型"""
    ext = Path(file_path).suffix.lower()
    
    for file_type, extensions in SUPPORTED_EXTENSIONS.items():
        if ext in extensions:
            return file_type
    return None

def validate_file_path(file_path: str) -> tuple[bool, str]:
    """
    验证文件路径的安全性和有效性
    
    推荐使用绝对路径，因为MCP Server和Client通常运行在不同的工作目录中。
    
    返回: (是否有效, 错误信息)
    """
    try:
        path = Path(file_path)
        
        # 推荐使用绝对路径
        if not path.is_absolute():
            # 尝试解析相对路径，但给出提示
            path = path.resolve()
            if not path.exists():
                return False, f"文件不存在：{file_path}\n💡 建议使用绝对路径，因为MCP Server和Client可能运行在不同目录中。\n   例如：{path}"
            else:
                # 相对路径找到了文件，但仍然建议使用绝对路径
                logger.warning(f"⚠️ 使用了相对路径 '{file_path}'，建议使用绝对路径 '{path}' 以确保可靠性")
        else:
            path = path.resolve()
        
        # 检查文件是否存在
        if not path.exists():
            return False, f"文件不存在：{file_path}"
        
        # 检查是否为文件
        if not path.is_file():
            return False, f"路径不是文件：{file_path}"
        
        # 检查文件类型
        file_type = get_file_type_from_extension(str(path))
        if not file_type:
            supported = ", ".join([f"{ft}({', '.join(exts)})" for ft, exts in SUPPORTED_EXTENSIONS.items()])
            return False, f"不支持的文件类型。支持的类型：{supported}"
        
        # 检查文件大小
        file_size = path.stat().st_size
        size_limit = FILE_SIZE_LIMITS[file_type]
        if file_size > size_limit:
            size_mb = size_limit // (1024 * 1024)
            return False, f"文件过大。{file_type}类型文件最大支持{size_mb}MB"
        
        return True, ""
        
    except Exception as e:
        return False, f"文件路径验证失败：{str(e)}"

async def process_file_upload(file_info: Dict[str, Any]) -> Dict[str, Any]:
    """
    处理文件上传
    
    参数:
    - file_info: 文件信息字典
    
    返回: 上传后的文件节点
    """
    file_type = file_info["file_type"]
    source_type = file_info["source_type"] 
    source_path = file_info["source_path"]
    metadata = file_info.get("metadata", {})
    
    logger.info(f"🔄 开始处理文件上传: {file_type}, {source_type}, {source_path}")
    
    # 预先检查API密钥
    try:
        get_mowen_api()  # 这会抛出异常如果API密钥未设置
    except RuntimeError as e:
        raise ValueError(f"API配置错误：{str(e)}。请设置MOWEN_API_KEY环境变量后重试。")
    
    try:
        if source_type == "local":
            # 本地文件上传
            is_valid, error_msg = validate_file_path(source_path)
            if not is_valid:
                raise ValueError(error_msg)
            
            file_path = Path(source_path)
            file_name = file_path.name
            file_type_code = FILE_TYPE_MAP[file_type]
            
            # 获取上传授权
            api_client = get_mowen_api()
            auth_result = await api_client.get_upload_auth(file_type_code, file_name)
            
            # 执行文件上传
            upload_result = await api_client.upload_file_local(auth_result, source_path)
            file_id = upload_result["file"]["fileId"]
            logger.info(f"✅ 文件上传成功，获得文件ID: {file_id}")
            
        elif source_type == "url":
            # 远程URL上传
            file_type_code = FILE_TYPE_MAP[file_type]
            file_name = metadata.get("file_name")
            
            api_client = get_mowen_api()
            upload_result = await api_client.upload_file_url(file_type_code, source_path, file_name)
            file_id = upload_result["file"]["fileId"]
            
        else:
            raise ValueError(f"不支持的上传类型：{source_type}")
        
        # 根据文件类型创建相应的节点
        if file_type == "image":
            alt = metadata.get("alt", "")
            align = metadata.get("align", "center")
            image_node = NoteAtomBuilder.create_image(file_id, alt, align)
            logger.info(f"🖼️ 创建图片节点: {image_node}")
            return image_node
        elif file_type == "audio":
            show_note = metadata.get("show_note", "")
            return NoteAtomBuilder.create_audio(file_id, show_note)
        elif file_type == "pdf":
            return NoteAtomBuilder.create_pdf(file_id)
        else:
            raise ValueError(f"不支持的文件类型：{file_type}")
            
    except Exception as e:
        logger.error(f"文件上传失败: {str(e)}")
        raise

async def process_paragraphs_with_files(paragraphs: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    处理包含文件的段落列表，将文件段落转换为实际的文件节点
    
    参数:
    - paragraphs: 段落列表
    
    返回: 处理后的段落列表
    """
    processed_paragraphs = []
    logger.info(f"📝 开始处理段落，总数: {len(paragraphs)}")
    
    for i, paragraph in enumerate(paragraphs):
        if paragraph.get("type") == "file":
            # 这是一个文件段落，需要上传文件并转换
            logger.info(f"📁 处理文件段落 {i}: {paragraph}")
            try:
                file_node = await process_file_upload(paragraph)
                processed_paragraphs.append(file_node)
                logger.info(f"✅ 文件段落 {i} 处理完成，生成节点: {file_node}")
            except Exception as e:
                # 文件上传失败，添加错误信息段落
                logger.error(f"❌ 文件段落 {i} 上传失败: {str(e)}")
                error_text = f"⚠️ 文件上传失败：{str(e)}"
                error_paragraph = NoteAtomBuilder.create_paragraph([
                    NoteAtomBuilder.create_text(error_text, [NoteAtomBuilder.create_highlight_mark()])
                ])
                processed_paragraphs.append(error_paragraph)
        else:
            # 普通段落，直接添加
            logger.info(f"📄 处理普通段落 {i}: {paragraph.get('type', 'paragraph')}")
            processed_paragraphs.append(paragraph)
    
    return processed_paragraphs

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
def create_note(
    paragraphs: List[Dict[str, Any]] = Field(
        description="""
        富文本段落列表，每个段落包含多个文本节点。支持文本、引用、内链笔记和文件。
        
        段落类型：
        1. 普通段落（默认）：{"texts": [...]}
        2. 引用段落：{"type": "quote", "texts": [...]}
        3. 内链笔记：{"type": "note", "note_id": "笔记ID"}
        4. 文件段落：{"type": "file", "file_type": "image|audio|pdf", "source_type": "local|url", "source_path": "路径", "metadata": {...}}
        
        格式示例：
        [
            {
                "texts": [
                    {"text": "这是普通文本"},
                    {"text": "这是加粗文本", "bold": true},
                    {"text": "这是高亮文本", "highlight": true},
                    {"text": "这是链接", "link": "https://example.com"}
                ]
            },
            {
                "type": "quote",
                "texts": [
                    {"text": "这是引用段落"},
                    {"text": "支持富文本", "bold": true}
                ]
            },
            {
                "type": "note",
                "note_id": "VPrWsE_-P0qwrFUOygGs8"
            },
            {
                "type": "file",
                "file_type": "image",
                "source_type": "local",
                "source_path": "/path/to/image.jpg",
                "metadata": {
                    "alt": "图片描述",
                    "align": "center"
                }
            },
            {
                "type": "file",
                "file_type": "audio",
                "source_type": "url",
                "source_path": "https://example.com/audio.mp3",
                "metadata": {
                    "show_note": "00:00 开场\\n01:30 主要内容"
                }
            },
            {
                "texts": [
                    {"text": "第二段内容"}
                ]
            }
        ]
        
        支持的文件类型：
        - 图片(image): .gif, .jpeg, .jpg, .png, .webp (最大50MB)
        - 音频(audio): .mp3, .mp4, .m4a (最大200MB)
        - PDF(pdf): .pdf (最大100MB)
        
        文件metadata说明：
        - 图片: alt(描述), align(对齐: left|center|right)
        - 音频: show_note(ShowNote内容)
        - PDF: 无需额外metadata
        
        ⚠️ 重要提示 - 文件路径要求：
        - 必须使用绝对路径，且保证路径完全正确
        - Windows示例: "C:\\Users\\用户名\\Documents\\image.jpg"
        - macOS/Linux示例: "/Users/用户名/Documents/image.jpg"
        
        如果只是简单文本，可以这样使用：
        [
            {
                "texts": [
                    {"text": "这是一段简单的文本内容"}
                ]
            }
        ]
        """
    ),
    auto_publish: bool = Field(default=False, description="是否自动发布笔记。True表示立即发布，False表示保存为草稿"),
    tags: Optional[List[str]] = Field(default=None, description="笔记标签列表，例如：['工作', '学习', '重要']")
) -> str:
    """
    创建一篇新的墨问笔记
    
    这个工具使用统一的富文本格式来创建笔记，支持：
    - 多个段落的结构化内容
    - 普通段落：文本格式（加粗、高亮、链接）
    - 引用段落：用于创建引用文本块，支持富文本格式
    - 内链笔记：引用其他笔记，创建笔记间的关联
    - 灵活的内容组织方式
    
    使用场景：
    - 快速记录想法或备忘录
    - 创建结构化文档
    - 保存会议记录或学习笔记
    - 包含外部链接的笔记
    
    简单文本示例：
    create_note(
        paragraphs=[
            {
                "texts": [
                    {"text": "今天学习了Python编程，重点是异步编程概念"}
                ]
            }
        ],
        auto_publish=True,
        tags=["学习", "Python", "编程"]
    )
    
    富文本示例：
    create_note(
        paragraphs=[
            {
                "texts": [
                    {"text": "重要提醒：", "bold": true},
                    {"text": "明天的会议已改期"}
                ]
            },
            {
                "type": "quote",
                "texts": [
                    {"text": "详情请查看：", "highlight": true},
                    {"text": "会议通知", "link": "https://example.com/meeting"}
                ]
            },
            {
                "type": "note",
                "note_id": "VPrWsE_-P0qwrFUOygGs8"
            }
        ],
        auto_publish=True,
        tags=["会议", "通知"]
    )

    注意：
    创建笔记时，尽量一次性传入所有内容，避免创建后再分多次调用edit接口
    """
    try:
        api_client = get_mowen_api()
    except RuntimeError as e:
        return f"错误：{str(e)}"
    
    # 参数验证
    if not validate_rich_note_paragraphs(paragraphs):
        return """❌ 参数格式错误！
        
正确的paragraphs格式示例：
[
    {
        "texts": [
            {"text": "普通文本"},
            {"text": "加粗文本", "bold": true},
            {"text": "高亮文本", "highlight": true},
            {"text": "链接文本", "link": "https://example.com"}
        ]
    },
    {
        "type": "quote",
        "texts": [
            {"text": "引用段落"}
        ]
    },
    {
        "type": "note",
        "note_id": "VPrWsE_-P0qwrFUOygGs8"
    }
]

请检查：
1. 普通段落和引用段落必须有"texts"字段
2. 内链笔记段落必须有"note_id"字段
3. 每个文本节点必须有"text"字段
4. bold和highlight必须是布尔值
5. link必须是字符串URL
6. note_id必须是字符串
"""
    
    if tags is None:
        tags = []
    
    try:
        # 先处理包含文件的段落，进行文件上传
        logger.info(f"🚀 开始创建笔记，原始段落数: {len(paragraphs)}")
        processed_paragraphs = run_async_safely(process_paragraphs_with_files(paragraphs))
        logger.info(f"📋 文件处理完成，处理后段落数: {len(processed_paragraphs)}")
        
        # 构建富文本内容
        paragraphs_built = []
        for para_data in processed_paragraphs:
            para_type = para_data.get("type", "paragraph")
            
            if para_type == "note":
                # 内链笔记节点
                note_id = para_data.get("note_id")
                if not note_id:
                    raise ValueError("内链笔记节点必须提供note_id参数")
                paragraphs_built.append(NoteAtomBuilder.create_note(note_id))
            elif para_type in ["image", "audio", "pdf"]:
                # 文件节点（已经通过process_paragraphs_with_files处理过）
                paragraphs_built.append(para_data)
            elif "texts" in para_data:
                # 文本段落（普通或引用）
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
                
                if para_type == "quote":
                    paragraphs_built.append(NoteAtomBuilder.create_quote(texts))
                else:
                    paragraphs_built.append(NoteAtomBuilder.create_paragraph(texts))
            else:
                # 其他类型的段落，可能是处理后的文件节点等，直接跳过或记录错误
                logger.warning(f"未知段落类型: {para_data}")
        
        body = NoteAtomBuilder.create_doc(paragraphs_built)
        settings = {
            "autoPublish": auto_publish,
            "tags": tags
        }
        
        # 记录最终发送给墨问的完整数据结构
        import json
        logger.info(f"🏗️ 最终构建的笔记结构:")
        logger.info(f"Body: {json.dumps(body, indent=2, ensure_ascii=False)}")
        logger.info(f"Settings: {json.dumps(settings, indent=2, ensure_ascii=False)}")
        
        # 详细记录每个阶段的段落数
        logger.info(f"📊 段落处理统计:")
        logger.info(f"  - 原始输入段落数: {len(paragraphs)}")
        logger.info(f"  - 文件处理后段落数: {len(processed_paragraphs)}")
        logger.info(f"  - 最终构建段落数: {len(paragraphs_built)}")
        logger.info(f"  - 每个构建段落的类型: {[p.get('type', 'unknown') for p in paragraphs_built]}")
        
        # 使用修复的异步运行方式
        result = run_async_safely(api_client.create_note(body, settings))
            
        return f"✅ 笔记创建成功！\n\n笔记ID: {result.get('noteId', 'N/A')}\n段落数: {len(paragraphs_built)}\n自动发布: {auto_publish}\n标签: {', '.join(tags)}"
    except httpx.HTTPStatusError as e:
        error_detail = ""
        try:
            error_json = e.response.json()
            error_detail = f"\n错误代码: {error_json.get('code', 'N/A')}\n错误原因: {error_json.get('reason', 'N/A')}\n错误信息: {error_json.get('message', 'N/A')}"
        except:
            error_detail = f"\nHTTP状态码: {e.response.status_code}"
            
        return f"❌ API调用失败: {str(e)}{error_detail}"
    except Exception as e:
        import traceback
        tb = traceback.format_exc()
        logger.error(f"创建笔记时发生错误: {str(e)}\n堆栈跟踪: {tb}")
        return f"❌ 发生错误: {str(e)}\n\n调试信息:\n{tb}"

@mcp.tool()
def edit_note(
    note_id: str = Field(description="要编辑的笔记ID，通常是创建笔记时返回的ID"),
    paragraphs: List[Dict[str, Any]] = Field(
        description="""
        富文本段落列表，每个段落包含多个文本节点。将完全替换原有笔记内容。支持文本、引用、内链笔记和文件。
        
        段落类型：
        1. 普通段落（默认）：{"texts": [...]}
        2. 引用段落：{"type": "quote", "texts": [...]}
        3. 内链笔记：{"type": "note", "note_id": "笔记ID"}
        4. 文件段落：{"type": "file", "file_type": "image|audio|pdf", "source_type": "local|url", "source_path": "路径", "metadata": {...}}
        
        格式示例：
        [
            {
                "texts": [
                    {"text": "这是普通文本"},
                    {"text": "这是加粗文本", "bold": true},
                    {"text": "这是高亮文本", "highlight": true},
                    {"text": "这是链接", "link": "https://example.com"}
                ]
            },
            {
                "type": "quote",
                "texts": [
                    {"text": "这是引用段落"},
                    {"text": "支持富文本", "bold": true}
                ]
            },
            {
                "type": "note",
                "note_id": "VPrWsE_-P0qwrFUOygGs8"
            },
            {
                "type": "file",
                "file_type": "image",
                "source_type": "local",
                "source_path": "/path/to/image.jpg",
                "metadata": {
                    "alt": "图片描述",
                    "align": "center"
                }
            },
            {
                "texts": [
                    {"text": "第二段内容"}
                ]
            }
        ]
        
        支持的文件类型：
        - 图片(image): .gif, .jpeg, .jpg, .png, .webp (最大50MB)
        - 音频(audio): .mp3, .mp4, .m4a (最大200MB)
        - PDF(pdf): .pdf (最大100MB)
        
        文件metadata说明：
        - 图片: alt(描述), align(对齐: left|center|right)
        - 音频: show_note(ShowNote内容)
        - PDF: 无需额外metadata
        
        如果只是简单文本，可以这样使用：
        [
            {
                "texts": [
                    {"text": "这是一段简单的文本内容"}
                ]
            }
        ]
        """
    )
) -> str:
    """
    编辑已存在的笔记内容
    
    这个工具使用统一的富文本格式来编辑笔记，支持：
    - 多个段落的结构化内容
    - 普通段落：文本格式（加粗、高亮、链接）
    - 引用段落：用于创建引用文本块，支持富文本格式
    - 内链笔记：引用其他笔记，创建笔记间的关联
    - 灵活的内容组织方式
    
    注意：此操作会完全替换笔记的原有内容，而不是追加内容。
    
    使用场景：
    - 修正笔记中的错误
    - 更新笔记内容
    - 将简单文本笔记升级为富文本格式
    - 重新组织笔记结构和格式
    
    简单文本示例：
    edit_note(
        note_id="note_123456",
        paragraphs=[
            {
                "texts": [
                    {"text": "更新后的笔记内容"}
                ]
            }
        ]
    )
    
    富文本示例：
    edit_note(
        note_id="note_123456",
        paragraphs=[
            {
                "texts": [
                    {"text": "更新：", "bold": true},
                    {"text": "项目进度已完成80%"}
                ]
            },
            {
                "type": "quote",
                "texts": [
                    {"text": "详细报告请查看：", "highlight": true},
                    {"text": "项目文档", "link": "https://example.com/report"}
                ]
            },
            {
                "type": "note",
                "note_id": "VPrWsE_-P0qwrFUOygGs8"
            }
        ]
    )
    """
    try:
        api_client = get_mowen_api()
    except RuntimeError as e:
        return f"错误：{str(e)}"
    
    # 参数验证
    if not validate_rich_note_paragraphs(paragraphs):
        return """❌ 参数格式错误！
        
正确的paragraphs格式示例：
[
    {
        "texts": [
            {"text": "普通文本"},
            {"text": "加粗文本", "bold": true},
            {"text": "高亮文本", "highlight": true},
            {"text": "链接文本", "link": "https://example.com"}
        ]
    },
    {
        "type": "quote",
        "texts": [
            {"text": "引用段落"}
        ]
    },
    {
        "type": "note",
        "note_id": "VPrWsE_-P0qwrFUOygGs8"
    }
]

请检查：
1. 普通段落和引用段落必须有"texts"字段
2. 内链笔记段落必须有"note_id"字段
3. 每个文本节点必须有"text"字段
4. bold和highlight必须是布尔值
5. link必须是字符串URL
6. note_id必须是字符串
"""
    
    try:
        # 先处理包含文件的段落，进行文件上传
        processed_paragraphs = run_async_safely(process_paragraphs_with_files(paragraphs))
        
        # 构建富文本内容
        paragraphs_built = []
        for para_data in processed_paragraphs:
            para_type = para_data.get("type", "paragraph")
            
            if para_type == "note":
                # 内链笔记节点
                note_id = para_data.get("note_id")
                if not note_id:
                    raise ValueError("内链笔记节点必须提供note_id参数")
                paragraphs_built.append(NoteAtomBuilder.create_note(note_id))
            elif para_type in ["image", "audio", "pdf"]:
                # 文件节点（已经通过process_paragraphs_with_files处理过）
                paragraphs_built.append(para_data)
            elif "texts" in para_data:
                # 文本段落（普通或引用）
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
                
                if para_type == "quote":
                    paragraphs_built.append(NoteAtomBuilder.create_quote(texts))
                else:
                    paragraphs_built.append(NoteAtomBuilder.create_paragraph(texts))
            else:
                # 其他类型的段落，可能是处理后的文件节点等，直接跳过或记录错误
                logger.warning(f"未知段落类型: {para_data}")
        
        body = NoteAtomBuilder.create_doc(paragraphs_built)
        
        # 使用修复的异步运行方式
        result = run_async_safely(api_client.edit_note(note_id, body))
            
        return f"✅ 笔记编辑成功！\n\n笔记ID: {result.get('noteId', note_id)}\n段落数: {len(paragraphs_built)}"
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
def set_note_privacy(
    note_id: str = Field(description="笔记ID"),
    privacy_type: Literal["public", "private", "rule"] = Field(
        description="""
        隐私类型：
        - 'public': 完全公开，任何人都可以访问
        - 'private': 私有，只有作者可以访问
        - 'rule': 规则公开，根据自定义规则控制访问
        """
    ),
    no_share: bool = Field(
        default=False, 
        description="当privacy_type为'rule'时，是否禁止分享。True表示禁止分享，False表示允许分享"
    ),
    expire_at: int = Field(
        default=0, 
        description="当privacy_type为'rule'时，过期时间戳（Unix时间戳）。0表示永不过期"
    )
) -> str:
    """
    设置笔记的隐私权限
    
    这个工具用于控制笔记的访问权限，支持三种模式：
    
    1. 完全公开（public）：任何人都可以访问
    2. 私有（private）：只有作者可以访问
    3. 规则公开（rule）：可以设置分享限制和过期时间
    
    使用场景：
    - 将草稿笔记设为公开
    - 保护敏感信息设为私有
    - 临时分享设置过期时间
    
    示例调用：
    # 设为完全公开
    set_note_privacy(note_id="note_123", privacy_type="public")
    
    # 设为私有
    set_note_privacy(note_id="note_123", privacy_type="private")
    
    # 设为规则公开，禁止分享，1小时后过期
    set_note_privacy(
        note_id="note_123", 
        privacy_type="rule", 
        no_share=True, 
        expire_at=1703980800
    )
    """
    try:
        api_client = get_mowen_api()
    except RuntimeError as e:
        return f"错误：{str(e)}"
    
    try:
        rule = None
        if privacy_type == "rule":
            rule = {
                "noShare": no_share,
                "expireAt": str(expire_at)
            }
        
        # 使用修复的异步运行方式
        result = run_async_safely(api_client.set_note_privacy(note_id, privacy_type, rule))
        
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
    """
    重置墨问API密钥
    
    ⚠️ 警告：此操作会立即使当前API密钥失效！
    
    使用场景：
    - API密钥泄露需要重置
    - 定期更换密钥提高安全性
    - 密钥丢失需要生成新的
    
    注意事项：
    1. 执行后当前密钥立即失效
    2. 需要立即保存新密钥
    3. 需要更新所有使用该密钥的应用
    
    示例调用：
    reset_api_key()
    """
    try:
        api_client = get_mowen_api()
    except RuntimeError as e:
        return f"错误：{str(e)}"
    
    try:
        # 使用修复的异步运行方式
        result = run_async_safely(api_client.reset_api_key())
            
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

# 添加参数验证辅助函数
def validate_rich_note_paragraphs(paragraphs: List[Dict[str, Any]]) -> bool:
    """验证富文本笔记段落格式"""
    try:
        for para in paragraphs:
            para_type = para.get("type", "paragraph")
            
            if para_type == "note":
                # 内链笔记节点验证
                if "note_id" not in para or not isinstance(para["note_id"], str):
                    return False
            elif para_type == "file":
                # 文件段落验证
                if "file_type" not in para or para["file_type"] not in ["image", "audio", "pdf"]:
                    return False
                if "source_type" not in para or para["source_type"] not in ["local", "url"]:
                    return False
                if "source_path" not in para or not isinstance(para["source_path"], str):
                    return False
                # metadata是可选的
                if "metadata" in para and not isinstance(para["metadata"], dict):
                    return False
            elif para_type in ["paragraph", "quote"] or "texts" in para:
                # 文本段落验证（普通段落或引用段落）
                if "texts" not in para:
                    return False
                for text in para["texts"]:
                    if "text" not in text or not isinstance(text["text"], str):
                        return False
                    # 验证可选字段
                    if "bold" in text and not isinstance(text["bold"], bool):
                        return False
                    if "highlight" in text and not isinstance(text["highlight"], bool):
                        return False
                    if "link" in text and not isinstance(text["link"], str):
                        return False
            # 如果都不匹配，可能是处理后的文件节点，跳过验证
        return True
    except:
        return False

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