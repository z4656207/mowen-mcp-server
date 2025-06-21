#!/bin/bash
# 配置助手 macOS 构建脚本

echo "🍎 构建配置助手 macOS 版本..."
echo "================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装或不在PATH中"
    echo "请先安装Python 3.8或更高版本"
    echo "推荐使用Homebrew: brew install python"
    exit 1
fi

echo "✅ Python环境检查通过"
python3 --version

# 检查PyInstaller
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "📦 正在安装PyInstaller..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "❌ PyInstaller安装失败"
        exit 1
    fi
fi

echo "✅ PyInstaller准备就绪"

# 清理旧的构建文件
rm -f "dist/配置助手"
rm -rf "build/配置助手"
rm -rf "dist/配置助手.app"

# 设置UTF-8环境变量
export LANG=zh_CN.UTF-8
export LC_ALL=zh_CN.UTF-8

# 开始构建
echo "🔨 开始打包配置助手..."
if [ -f "配置助手_utf8.spec" ]; then
    echo "📋 使用自定义spec文件构建..."
    pyinstaller --clean --noconfirm "配置助手_utf8.spec"
else
    echo "📋 使用默认参数构建..."
    pyinstaller --onefile --windowed --name "配置助手" --clean --noconfirm --hidden-import=encodings.utf_8 config_helper.py
fi

# 检查构建结果
if [ -f "dist/配置助手" ] || [ -d "dist/配置助手.app" ]; then
    echo "✅ 配置助手构建成功！"
    
    # 拷贝到发布目录
    echo ""
    echo "📦 拷贝到发布目录..."
    
    # 确保发布目录存在
    if [ ! -d "../release/macos-release" ]; then
        echo "📁 创建发布目录: ../release/macos-release"
        mkdir -p "../release/macos-release"
    fi
    
    if [ ! -d "../release/macos-release/user-version" ]; then
        echo "📁 创建用户版本目录: ../release/macos-release/user-version"
        mkdir -p "../release/macos-release/user-version"
    fi
    
    # 处理可执行文件
    if [ -f "dist/配置助手" ]; then
        echo "📁 输出文件: dist/配置助手"
        echo "📏 文件大小: $(ls -lh dist/配置助手 | awk '{print $5}')"
        
        # 设置执行权限
        chmod +x "dist/配置助手"
        echo "🔐 已设置执行权限"
        
        # 拷贝可执行文件到发布目录
        echo "正在拷贝可执行文件..."
        cp "dist/配置助手" "../release/macos-release/user-version/配置助手"
        if [ $? -eq 0 ]; then
            chmod +x "../release/macos-release/user-version/配置助手"
            echo "✅ 已拷贝可执行文件到: ../release/macos-release/user-version/配置助手"
            
            # 验证拷贝结果
            if [ -f "../release/macos-release/user-version/配置助手" ]; then
                target_size=$(ls -l "../release/macos-release/user-version/配置助手" | awk '{print $5}')
                echo "📏 目标文件大小: $target_size 字节"
            fi
        else
            echo "❌ 拷贝可执行文件到发布目录失败"
        fi
    fi
    
    # 处理.app应用包
    if [ -d "dist/配置助手.app" ]; then
        echo "📁 输出应用: dist/配置助手.app"
        echo "📏 应用大小: $(du -sh dist/配置助手.app | awk '{print $1}')"
        
        # 拷贝.app应用到发布目录
        echo "正在拷贝应用包..."
        cp -r "dist/配置助手.app" "../release/macos-release/user-version/配置助手.app"
        if [ $? -eq 0 ]; then
            echo "✅ 已拷贝应用包到: ../release/macos-release/user-version/配置助手.app"
            
            # 验证拷贝结果
            if [ -d "../release/macos-release/user-version/配置助手.app" ]; then
                target_app_size=$(du -sh "../release/macos-release/user-version/配置助手.app" | awk '{print $1}')
                echo "📏 目标应用大小: $target_app_size"
            fi
        else
            echo "❌ 拷贝应用包到发布目录失败"
        fi
    fi
    
    echo ""
    echo "💡 使用说明:"
    echo "   方式一: 双击运行 配置助手.app (如果生成了.app文件)"
    echo "   方式二: 在终端运行 ./dist/配置助手"
    echo "   然后:"
    echo "   1. 输入墨问API密钥"
    echo "   2. 点击"生成配置"按钮"
    echo "   3. 复制生成的配置到Cursor等客户端"
    echo ""
    echo "🎉 构建完成！"
else
    echo "❌ 构建失败，请检查错误信息"
    exit 1
fi