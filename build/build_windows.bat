@echo off
REM Windows平台构建脚本

REM 设置控制台编码为UTF-8，避免中文乱码
chcp 65001 >nul

echo 🪟 构建Windows版本...
python build_release.py --platform windows

if %errorlevel% equ 0 (
    echo ✅ Windows版本构建完成！
) else (
    echo ❌ 构建失败
    echo 请检查错误信息并重试
)
echo.
echo 按任意键退出...
pause >nul 