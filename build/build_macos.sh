#!/bin/bash
# macOS平台构建脚本

# 设置UTF-8环境变量，避免中文乱码
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

echo "🍎 构建macOS版本..."
python3 build_release.py --platform macos

if [ $? -eq 0 ]; then
    echo "✅ macOS版本构建完成！"
else
    echo "❌ 构建失败"
fi

read -p "按回车键退出..." 