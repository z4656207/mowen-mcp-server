#!/bin/bash
# 墨问 MCP 服务器安装脚本

echo "🚀 正在安装墨问 MCP 服务器..."

# 检查Python版本
echo "📋 检查Python版本..."
python_version=$(python --version 2>&1 | grep -oP '(?<=Python )\d+\.\d+')
required_version="3.8"

if [[ "$(printf '%s\n' "$required_version" "$python_version" | sort -V | head -n1)" != "$required_version" ]]; then
    echo "❌ 需要Python 3.8或更高版本，当前版本: $python_version"
    exit 1
fi

echo "✅ Python版本检查通过: $python_version"

# 安装依赖
echo "📦 安装项目依赖..."
pip install -e .

if [ $? -eq 0 ]; then
    echo "✅ 安装完成！"
    echo ""
    echo "📝 下一步："
    echo "1. 设置API密钥："
    echo "   export MOWEN_API_KEY=\"你的墨问API密钥\""
    echo ""
    echo "2. 在Cursor中配置MCP服务器："
    echo '   "mowen-mcp-server": {'
    echo '     "command": "python",'
    echo '     "args": ["-m", "mowen_mcp_server.server"],'
    echo '     "env": {'
    echo '       "MOWEN_API_KEY": "${env:MOWEN_API_KEY}"'
    echo '     }'
    echo '   }'
    echo ""
    echo "🎉 安装成功！"
else
    echo "❌ 安装失败，请检查错误信息"
    exit 1
fi 