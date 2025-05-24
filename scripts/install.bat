@echo off
REM 墨问 MCP 服务器 Windows 安装脚本

echo 🚀 正在安装墨问 MCP 服务器...

REM 检查Python版本
echo 📋 检查Python版本...
python --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Python未安装或不在PATH中
    echo 请先安装Python 3.8或更高版本
    pause
    exit /b 1
)

echo ✅ Python检查通过

REM 安装依赖
echo 📦 安装项目依赖...
pip install -e .

if %errorlevel% equ 0 (
    echo ✅ 安装完成！
    echo.
    echo 📝 下一步：
    echo 1. 设置API密钥：
    echo    $env:MOWEN_API_KEY="你的墨问API密钥"
    echo.
    echo 2. 在Cursor中配置MCP服务器：
    echo    "mowen-mcp-server": {
    echo      "command": "python",
    echo      "args": ["-m", "mowen_mcp_server.server"],
    echo      "env": {
    echo        "MOWEN_API_KEY": "${env:MOWEN_API_KEY}"
    echo      }
    echo    }
    echo.
    echo 🎉 安装成功！
) else (
    echo ❌ 安装失败，请检查错误信息
    pause
    exit /b 1
)

pause 