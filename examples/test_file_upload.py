#!/usr/bin/env python3
"""
墨问MCP服务社区版文件上传功能测试示例

这个脚本演示如何使用墨问MCP服务社区版的文件上传功能。
包含本地文件上传和远程URL上传两种方式的示例。

使用前请确保：
1. 已设置 MOWEN_API_KEY 环境变量
2. 已安装必要的依赖：pip install aiofiles
3. 准备好测试用的本地文件（必须使用绝对路径）
"""

import os
import asyncio
from src.mowen_mcp_server.server import MowenAPI, process_paragraphs_with_files, NoteAtomBuilder

async def test_file_upload():
    """测试文件上传功能"""
    
    # 初始化API客户端
    api_key = os.getenv("MOWEN_API_KEY")
    if not api_key:
        print("❌ 请先设置 MOWEN_API_KEY 环境变量")
        return
    
    api = MowenAPI(api_key)
    print("✅ API客户端初始化成功")
    
    # 测试1：通过URL上传图片
    print("\n🔄 测试1：通过URL上传图片...")
    try:
        result = await api.upload_file_url(
            file_type=1,  # 图片
            url="https://httpbin.org/image/png",
            file_name="测试图片.png"
        )
        print(f"✅ URL上传成功！文件ID: {result['file']['fileId']}")
        image_file_id = result['file']['fileId']
    except Exception as e:
        print(f"❌ URL上传失败: {str(e)}")
        image_file_id = None
    
    # 测试2：创建包含文件的笔记
    print("\n🔄 测试2：创建包含文件的笔记...")
    try:
        # 构造包含文件的段落
        paragraphs = [
            {
                "texts": [
                    {"text": "文件上传功能测试", "bold": True}
                ]
            },
            {
                "texts": [
                    {"text": "以下是通过不同方式上传的文件："}
                ]
            }
        ]
        
        # 如果URL上传成功，添加图片文件
        if image_file_id:
            paragraphs.append({
                "type": "file",
                "file_type": "image",
                "source_type": "uploaded",  # 已上传的文件
                "file_id": image_file_id,
                "metadata": {
                    "alt": "测试图片",
                    "align": "center"
                }
            })
        
                 # 添加本地文件示例（如果有的话）
         # 注意：这里演示的是段落中的文件上传，不是直接调用API
         # 本地文件会在 process_paragraphs_with_files 中自动处理
        
        # 尝试从URL上传音频（演示用）
        paragraphs.append({
            "type": "file",
            "file_type": "audio",
            "source_type": "url",
            "source_path": "https://www.soundjay.com/misc/sounds/bell-ringing-05.wav",
            "metadata": {
                "show_note": "00:00 铃声测试"
            }
        })
        
        # 处理文件上传
        processed_paragraphs = await process_paragraphs_with_files(paragraphs)
        
        # 构建笔记内容
        note_content = []
        for para in processed_paragraphs:
            para_type = para.get("type", "paragraph")
            if para_type in ["image", "audio", "pdf"]:
                note_content.append(para)
            elif para_type == "note":
                note_content.append(NoteAtomBuilder.create_note(para["note_id"]))
            else:
                texts = []
                for text_data in para["texts"]:
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
                
                note_content.append(NoteAtomBuilder.create_paragraph(texts))
        
        body = NoteAtomBuilder.create_doc(note_content)
        
        # 创建笔记
        create_result = await api.create_note(body, {
            "autoPublish": True,
            "tags": ["测试", "文件上传", "MCP"]
        })
        
        print(f"✅ 笔记创建成功！笔记ID: {create_result['noteId']}")
        
    except Exception as e:
        print(f"❌ 笔记创建失败: {str(e)}")

def main():
    """主函数"""
    print("📁 墨问MCP服务社区版文件上传功能测试")
    print("=" * 50)
    
    # 运行异步测试
    asyncio.run(test_file_upload())
    
    print("\n🎉 测试完成！")
    print("\n💡 使用提示：")
    print("1. 在创建笔记时，可以混合使用文本和文件段落")
    print("2. 本地文件必须使用绝对路径（如 C:\\Users\\user\\file.jpg）")
    print("3. 远程URL需要确保可以访问且文件格式支持")
    print("4. 文件会自动进行类型和大小验证")
    print("5. MCP Server与Client运行在不同目录，相对路径会失效")

if __name__ == "__main__":
    main() 