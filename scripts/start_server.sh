#!/bin/bash
# 启动墨问 MCP 服务器脚本

# 检查 API 密钥
if [ -z "$MOWEN_API_KEY" ]; then
    echo "❌ 错误：未设置 MOWEN_API_KEY 环境变量"
    echo "请运行: export MOWEN_API_KEY=your_api_key_here"
    exit 1
fi

echo "🚀 启动墨问 MCP 服务器..."
echo "📝 API 密钥: ${MOWEN_API_KEY:0:10}..."

# 启动服务器
python -m mowen_mcp_server.server 