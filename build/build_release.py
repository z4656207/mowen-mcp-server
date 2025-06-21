"""
墨问MCP服务社区版跨平台发布构建脚本

支持平台：
- Windows (exe文件)
- macOS (app文件)
- Linux (可执行文件)

使用方法：
python build_release.py [--platform windows|macos|linux|all]
"""

import subprocess
import sys
import os
import shutil
import json
import platform
import argparse
from pathlib import Path

class CrossPlatformBuilder:
    def __init__(self):
        self.project_root = Path(__file__).parent.parent
        self.build_dir = Path(__file__).parent
        self.release_dir = self.project_root / "release"
        self.current_platform = platform.system().lower()
        
        # 平台特定配置
        self.platform_configs = {
            'windows': {
                'exe_suffix': '.exe',
                'pyinstaller_args': ['--console'],
                'main_name': 'mowen-mcp-server.exe'
            },
            'darwin': {  # macOS
                'exe_suffix': '',
                'pyinstaller_args': ['--console'],
                'main_name': 'mowen-mcp-server'
            },
            'linux': {
                'exe_suffix': '',
                'pyinstaller_args': ['--console'],
                'main_name': 'mowen-mcp-server'
            }
        }
        
    def build_all_platforms(self):
        """构建所有支持的平台"""
        print("🌍 开始跨平台构建...")
        
        if self.current_platform == 'windows':
            self.build_platform('windows')
        elif self.current_platform == 'darwin':
            self.build_platform('macos')
        elif self.current_platform == 'linux':
            self.build_platform('linux')
        else:
            print(f"⚠️ 当前平台 {self.current_platform} 可能不完全支持")
            self.build_platform(self.current_platform)
            
    def build_platform(self, target_platform):
        """构建指定平台"""
        print(f"\n🚀 构建 {target_platform.upper()} 版本...")
        
        # 创建发布目录，如果存在则不操作
        platform_release_dir = self.release_dir / f"{target_platform}-release"
        platform_release_dir.mkdir(parents=True, exist_ok=True)
        
        # 构建开发者版本和用户版本
        self.build_developer_version(platform_release_dir, target_platform)
        self.build_user_version(platform_release_dir, target_platform)
        
        print(f"✅ {target_platform.upper()} 版本构建完成！")
        
    def build_developer_version(self, platform_dir, target_platform):
        """构建开发者版本"""
        print(f"📦 构建 {target_platform} 开发者版本...")
        
        dev_dir = platform_dir / "developer-version"
        if dev_dir.exists():
            shutil.rmtree(dev_dir)
        dev_dir.mkdir()
        
        # 复制项目文件
        shutil.copytree(self.project_root / "src", dev_dir / "src")
        shutil.copytree(self.project_root / "scripts", dev_dir / "scripts")
        shutil.copy2(self.project_root / "pyproject.toml", dev_dir)
        shutil.copy2(self.project_root / "README.md", dev_dir)
        shutil.copy2(self.project_root / "LICENSE", dev_dir)
        shutil.copy2(self.project_root / "env.example", dev_dir)
        
        # 创建平台特定的安装说明
        self.create_platform_dev_guide(dev_dir, target_platform)
        
        print(f"✅ {target_platform} 开发者版本完成")
        
    def build_user_version(self, platform_dir, target_platform):
        """构建用户版本"""
        print(f"📦 构建 {target_platform} 用户版本...")
        
        user_dir = platform_dir / "user-version"
        user_dir.mkdir(exist_ok=True)
        
        print(f"📁 用户版本目录: {user_dir}")
        
        # 确保PyInstaller已安装
        self.ensure_pyinstaller()
        
        # 构建主程序
        if self.build_main_executable(user_dir, target_platform):
            print("✅ 主程序构建成功")
            
            # 验证构建结果
            self.verify_user_version_build(user_dir, target_platform)
            
            # 创建用户指南和辅助文件
            self.create_user_guide(user_dir, target_platform)
            self.create_platform_scripts(user_dir, target_platform)
            
            print(f"✅ {target_platform} 用户版本完成")
        else:
            print(f"❌ {target_platform} 用户版本构建失败")
            
    def ensure_pyinstaller(self):
        """确保PyInstaller已安装"""
        try:
            import PyInstaller
            print("✅ PyInstaller已安装")
        except ImportError:
            print("📦 正在安装PyInstaller...")
            subprocess.run([sys.executable, "-m", "pip", "install", "pyinstaller"])
            
    def build_main_executable(self, user_dir, target_platform):
        """构建主程序可执行文件"""
        print(f"🔨 打包 {target_platform} 主程序...")
        
        # 获取平台配置
        platform_key = 'darwin' if target_platform == 'macos' else target_platform
        config = self.platform_configs.get(platform_key, self.platform_configs['linux'])
        
        # PyInstaller命令
        cmd = [
            "pyinstaller",
            "--onefile",
            "--name", "mowen-mcp-server",
            "--clean",
            "--noconfirm"
        ] + config['pyinstaller_args'] + [
            str(self.project_root / "src" / "mowen_mcp_server" / "server.py")
        ]
        
        # 执行构建
        result = subprocess.run(cmd, cwd=str(self.project_root), 
                              capture_output=True, text=True, encoding='utf-8', errors='ignore')
        
        if result.returncode == 0:
            # 查找生成的文件
            dist_dir = self.project_root / "dist"
            if target_platform == 'macos':
                # macOS可能生成.app文件或普通可执行文件
                exe_files = list(dist_dir.glob("mowen-mcp-server*"))
            else:
                exe_files = [dist_dir / f"mowen-mcp-server{config['exe_suffix']}"]
            
            # 复制可执行文件
            for exe_file in exe_files:
                if exe_file.exists():
                    target_name = config['main_name']
                    shutil.copy2(exe_file, user_dir / target_name)
                    
                    # macOS需要设置执行权限
                    if target_platform == 'macos':
                        os.chmod(user_dir / target_name, 0o755)
                    
                    print(f"✅ 主程序打包完成: {target_name}")
                    return True
                    
            print("❌ 找不到生成的可执行文件")
            return False
        else:
            print("❌ 主程序打包失败:")
            print(result.stderr)
            return False
            

    def verify_user_version_build(self, user_dir, target_platform):
        """验证用户版本构建结果"""
        print(f"\n🔍 验证 {target_platform} 用户版本构建结果:")
        
        platform_key = 'darwin' if target_platform == 'macos' else target_platform
        config = self.platform_configs.get(platform_key, self.platform_configs['linux'])
        
        main_exe = user_dir / config['main_name']
        
        print(f"  📋 检查文件:")
        print(f"    主程序: {'✅' if main_exe.exists() else '❌'} {main_exe}")
        if main_exe.exists():
            size = main_exe.stat().st_size / (1024*1024)  # MB
            print(f"           大小: {size:.1f} MB")
        
        # 列出用户版本目录的所有文件
        print(f"  📁 用户版本目录内容:")
        for item in sorted(user_dir.iterdir()):
            item_type = "📁" if item.is_dir() else "📄"
            print(f"    {item_type} {item.name}")
        
    def create_platform_dev_guide(self, dev_dir, target_platform):
        """创建平台特定的开发者指南"""
        if target_platform == 'windows':
            guide_content = """# 墨问MCP服务社区版 - Windows开发者版本

## 安装方式

### 方式一：使用安装脚本（推荐）
双击 `scripts/install.bat`

### 方式二：手动安装
```cmd
pip install -e .
```

## 配置方式

在Cursor中配置：
```json
{
  "mcpServers": {
    "mowen-mcp-server": {
      "command": "python",
      "args": ["-m", "mowen_mcp_server.server"],
      "env": {
        "MOWEN_API_KEY": "${env:MOWEN_API_KEY}"
      }
    }
  }
}
```

## 设置API密钥

PowerShell:
```powershell
$env:MOWEN_API_KEY="你的API密钥"
```

详细文档请参考 README.md
"""
        elif target_platform == 'macos':
            guide_content = """# 墨问MCP服务社区版 - macOS开发者版本

## 安装方式

### 方式一：使用安装脚本（推荐）
```bash
bash scripts/install.sh
```

### 方式二：手动安装
```bash
pip install -e .
```

## 配置方式

在Cursor中配置：
```json
{
  "mcpServers": {
    "mowen-mcp-server": {
      "command": "python",
      "args": ["-m", "mowen_mcp_server.server"],
      "env": {
        "MOWEN_API_KEY": "${env:MOWEN_API_KEY}"
      }
    }
  }
}
```

## 设置API密钥

Terminal:
```bash
export MOWEN_API_KEY="你的API密钥"
```

持久化设置（添加到 ~/.zshrc 或 ~/.bash_profile）:
```bash
echo 'export MOWEN_API_KEY="你的API密钥"' >> ~/.zshrc
```

详细文档请参考 README.md
"""
        else:  # Linux
            guide_content = """# 墨问MCP服务社区版 - Linux开发者版本

## 安装方式

### 方式一：使用安装脚本（推荐）
```bash
bash scripts/install.sh
```

### 方式二：手动安装
```bash
pip install -e .
```

## 配置方式

在Cursor中配置：
```json
{
  "mcpServers": {
    "mowen-mcp-server": {
      "command": "python",
      "args": ["-m", "mowen_mcp_server.server"],
      "env": {
        "MOWEN_API_KEY": "${env:MOWEN_API_KEY}"
      }
    }
  }
}
```

## 设置API密钥

```bash
export MOWEN_API_KEY="你的API密钥"
```

持久化设置（添加到 ~/.bashrc）:
```bash
echo 'export MOWEN_API_KEY="你的API密钥"' >> ~/.bashrc
```

详细文档请参考 README.md
"""
        
        with open(dev_dir / "安装说明.md", "w", encoding="utf-8") as f:
            f.write(guide_content)
            
    def create_user_guide(self, user_dir, target_platform):
        """创建用户指南"""
        platform_names = {
            'windows': 'Windows',
            'macos': 'macOS', 
            'linux': 'Linux'
        }
        
        platform_name = platform_names.get(target_platform, target_platform.title())
        
        if target_platform == 'windows':
            main_exe_name = "mowen-mcp-server.exe"
        elif target_platform == 'macos':
            main_exe_name = "mowen-mcp-server"
        else:
            main_exe_name = "mowen-mcp-server"

        guide_content = f"""# 墨问MCP服务社区版 - {platform_name}用户版本

## 🚀 快速开始

### 第1步：获取API密钥
1. 打开墨问小程序
2. 进入"个人主页" → "开发者"
3. 复制您的API密钥

### 第2步：在Cursor中配置
将以下配置复制到Cursor的MCP设置中，并替换 "你的API密钥"。

**重要提示**: `command`中的`"完整路径/{main_exe_name}"` 需要替换为`mowen-mcp-server`可执行文件的实际绝对路径。

```json
{{{{
  "mcpServers": {{{{
    "mowen-mcp-server": {{{{
      "command": "完整路径/{main_exe_name}",
      "args": [],
      "env": {{{{
        "MOWEN_API_KEY": "你的API密钥"
      }}}}
    }}}}
  }}}}
}}}}
```

## ✨ 使用说明

配置完成后，在Trae或Cursor中可以直接使用：
- 创建墨问笔记
- 编辑笔记内容
- 上传图片、音频、PDF文件
- 设置笔记权限

## 📁 文件说明

- `{main_exe_name}`: 主程序（由Trae或Cursor自动调用）
- `用户指南.md`: 本文件

## 🔧 手动配置

Cursor配置格式：
```json
{{{{
  "mcpServers": {{{{
    "mowen-mcp-server": {{{{
      "command": "完整路径/{main_exe_name}",
      "args": [],
      "env": {{{{
        "MOWEN_API_KEY": "您的API密钥"
      }}}}
    }}}}
  }}}}
}}}}
```

## 🆘 常见问题

**Q: 提示找不到文件？**
A: 确保可执行文件和用户指南在同一个目录下，并检查Cursor配置中的`command`路径是否正确。

**Q: API调用失败？**  
A: 检查API密钥是否正确，确保有墨问Pro会员权限

{"**Q: 系统提示文件不安全？**" if target_platform == "macos" else ""}
{"A: 在系统偏好设置 → 安全性与隐私中允许运行" if target_platform == "macos" else ""}

## 📞 获取帮助

- 项目主页: https://github.com/z4656207/mowen-mcp-server
- 问题反馈: 在GitHub上提交Issue

---
本程序完全免费开源，如有帮助请给项目点个Star ⭐
"""
        
        with open(user_dir / "用户指南.md", "w", encoding="utf-8") as f:
            f.write(guide_content)
            
    def create_platform_scripts(self, user_dir, target_platform):
        """创建平台特定的辅助脚本"""
        if target_platform == 'windows':
            # Windows测试脚本
            test_script = '''@echo off
REM 墨问MCP服务社区版测试启动脚本
REM 设置控制台编码
chcp 65001 >nul

echo 🧪 墨问MCP服务社区版测试启动
echo.

echo 📋 检查文件...
if not exist "mowen-mcp-server.exe" (
    echo ❌ 找不到 mowen-mcp-server.exe
    echo 请确保在正确的目录中运行此脚本
    pause
    exit /b 1
)

echo ✅ 文件检查通过
echo.
echo 🚀 启动服务器（测试模式）...
echo 💡 正常使用时，此程序由Cursor自动调用
echo 💡 如需停止，请按 Ctrl+C
echo.

mowen-mcp-server.exe

echo.
echo 🔚 程序已退出
pause
'''
            with open(user_dir / "测试启动.bat", "w", encoding="utf-8") as f:
                f.write(test_script)
                


                
        elif target_platform == 'macos':
            # macOS测试脚本
            test_script = '''#!/bin/bash
echo "🧪 墨问MCP服务社区版测试启动"

echo "📋 检查文件..."
if [ ! -f "mowen-mcp-server" ]; then
    echo "❌ 找不到 mowen-mcp-server"
    read -p "按回车键退出..."
    exit 1
fi

echo "✅ 文件检查通过"
echo "🚀 启动服务器（测试模式）..."
echo "💡 正常使用时，此程序由Cursor自动调用"

./mowen-mcp-server

echo "🔚 程序已退出"
read -p "按回车键退出..."
'''
            test_file = user_dir / "测试启动.sh"
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_script)
            os.chmod(test_file, 0o755)  # 设置执行权限
            
        else:  # Linux
            # Linux测试脚本
            test_script = '''#!/bin/bash
echo "🧪 墨问MCP服务社区版测试启动"

echo "📋 检查文件..."
if [ ! -f "mowen-mcp-server" ]; then
    echo "❌ 找不到 mowen-mcp-server"
    read -p "按回车键退出..."
    exit 1
fi

echo "✅ 文件检查通过"
echo "🚀 启动服务器（测试模式）..."
echo "💡 正常使用时，此程序由Cursor自动调用"

./mowen-mcp-server

echo "🔚 程序已退出"
read -p "按回车键退出..."
'''
            test_file = user_dir / "测试启动.sh"
            with open(test_file, "w", encoding="utf-8") as f:
                f.write(test_script)
            os.chmod(test_file, 0o755)  # 设置执行权限
            
    def cleanup(self):
        """清理构建临时文件"""
        print("🧹 清理临时文件...")
        
        temp_paths = [
            self.project_root / "build",
            self.project_root / "dist"
        ]
        
        # 清理.spec文件
        for spec_file in self.project_root.glob("*.spec"):
            spec_file.unlink()
            
        for temp_path in temp_paths:
            if temp_path.exists() and temp_path != self.build_dir:
                shutil.rmtree(temp_path)

def main():
    parser = argparse.ArgumentParser(description='墨问MCP服务社区版跨平台构建工具')
    parser.add_argument('--platform', 
                       choices=['windows', 'macos', 'linux', 'all'],
                       default='current',
                       help='目标平台 (默认: 当前平台)')
    
    args = parser.parse_args()
    
    builder = CrossPlatformBuilder()
    
    try:
        if args.platform == 'all':
            print("⚠️ 注意：跨平台构建需要在对应平台上运行")
            print("当前只能构建当前平台的版本")
            builder.build_all_platforms()
        elif args.platform == 'current':
            builder.build_all_platforms()
        else:
            if args.platform == 'macos' and builder.current_platform != 'darwin':
                print("⚠️ 警告：在非macOS平台构建macOS版本可能不完全兼容")
            builder.build_platform(args.platform)
    finally:
        builder.cleanup()

if __name__ == "__main__":
    main()