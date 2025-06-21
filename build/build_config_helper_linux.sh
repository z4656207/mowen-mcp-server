#!/bin/bash
# 配置助手 Linux 构建脚本

echo "🐧 构建配置助手 Linux 版本..."
echo "================================"

# 检查Python环境
if ! command -v python3 &> /dev/null; then
    echo "❌ Python3未安装或不在PATH中"
    echo "请先安装Python 3.8或更高版本"
    echo "Ubuntu/Debian: sudo apt install python3 python3-pip"
    echo "CentOS/RHEL: sudo yum install python3 python3-pip"
    echo "Arch Linux: sudo pacman -S python python-pip"
    exit 1
fi

echo "✅ Python环境检查通过"
python3 --version

# 检查tkinter支持
if ! python3 -c "import tkinter" &> /dev/null; then
    echo "❌ tkinter未安装，这是GUI应用必需的"
    echo "Ubuntu/Debian: sudo apt install python3-tk"
    echo "CentOS/RHEL: sudo yum install tkinter"
    echo "Arch Linux: tkinter包含在python包中"
    exit 1
fi

echo "✅ tkinter支持检查通过"

# 检查PyInstaller
if ! python3 -c "import PyInstaller" &> /dev/null; then
    echo "📦 正在安装PyInstaller..."
    pip3 install pyinstaller
    if [ $? -ne 0 ]; then
        echo "❌ PyInstaller安装失败"
        echo "尝试使用用户安装: pip3 install --user pyinstaller"
        pip3 install --user pyinstaller
        if [ $? -ne 0 ]; then
            echo "❌ PyInstaller安装仍然失败"
            exit 1
        fi
    fi
fi

echo "✅ PyInstaller准备就绪"

# 清理旧的构建文件
rm -f "dist/配置助手"
rm -rf "build/配置助手"

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
if [ -f "dist/配置助手" ]; then
    echo "✅ 配置助手构建成功！"
    echo "📁 输出文件: dist/配置助手"
    echo "📏 文件大小: $(ls -lh dist/配置助手 | awk '{print $5}')"
    
    # 设置执行权限
    chmod +x "dist/配置助手"
    echo "🔐 已设置执行权限"
    
    # 拷贝到发布目录
    echo ""
    echo "📦 拷贝到发布目录..."
    
    # 确保发布目录存在
    if [ ! -d "../release/linux-release" ]; then
        echo "📁 创建发布目录: ../release/linux-release"
        mkdir -p "../release/linux-release"
    fi
    
    if [ ! -d "../release/linux-release/user-version" ]; then
        echo "📁 创建用户版本目录: ../release/linux-release/user-version"
        mkdir -p "../release/linux-release/user-version"
    fi
    
    # 拷贝配置助手到发布目录
    echo "正在拷贝文件..."
    cp "dist/配置助手" "../release/linux-release/user-version/配置助手"
    if [ $? -eq 0 ]; then
        chmod +x "../release/linux-release/user-version/配置助手"
        echo "✅ 已拷贝到: ../release/linux-release/user-version/配置助手"
        
        # 验证拷贝结果
        if [ -f "../release/linux-release/user-version/配置助手" ]; then
            target_size=$(ls -l "../release/linux-release/user-version/配置助手" | awk '{print $5}')
            echo "📏 目标文件大小: $target_size 字节"
        fi
    else
        echo "❌ 拷贝到发布目录失败"
        echo "请检查权限或手动拷贝文件"
    fi
    
    echo ""
    echo "💡 使用说明:"
    echo "   在终端运行: ./dist/配置助手"
    echo "   或者双击文件管理器中的可执行文件"
    echo "   然后:"
    echo "   1. 输入墨问API密钥"
    echo "   2. 点击"生成配置"按钮"
    echo "   3. 复制生成的配置到Cursor等客户端"
    echo ""
    echo "📋 系统要求:"
    echo "   - 需要X11显示服务器（桌面环境）"
    echo "   - 如果在服务器环境，需要配置X11转发"
    echo ""
    echo "🎉 构建完成！"
else
    echo "❌ 构建失败，请检查错误信息"
    echo ""
    echo "🔧 常见问题解决:"
    echo "   1. 确保安装了python3-tk包"
    echo "   2. 确保有GUI环境或X11转发"
    echo "   3. 检查PyInstaller是否正确安装"
    exit 1
fi