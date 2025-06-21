#!/usr/bin/env python3
"""
配置助手跨平台构建脚本

支持平台：
- Windows (exe文件)
- macOS (app文件/可执行文件)
- Linux (可执行文件)

使用方法：
python build_config_helper.py [--platform windows|macos|linux|all]
"""

import subprocess
import sys
import os
import shutil
import platform
import argparse
from pathlib import Path

class ConfigHelperBuilder:
    def __init__(self):
        self.build_dir = Path(__file__).parent
        self.current_platform = platform.system().lower()
        
        # 平台特定配置
        self.platform_configs = {
            'windows': {
                'exe_suffix': '.exe',
                'pyinstaller_args': ['--windowed'],
                'output_name': '配置助手.exe',
                'python_cmd': 'python'
            },
            'darwin': {  # macOS
                'exe_suffix': '',
                'pyinstaller_args': ['--windowed'],
                'output_name': '配置助手',
                'python_cmd': 'python3'
            },
            'linux': {
                'exe_suffix': '',
                'pyinstaller_args': ['--windowed'],
                'output_name': '配置助手',
                'python_cmd': 'python3'
            }
        }
        
    def check_environment(self, target_platform):
        """检查构建环境"""
        print(f"🔍 检查 {target_platform} 构建环境...")
        
        # 获取平台配置
        platform_key = 'darwin' if target_platform == 'macos' else target_platform
        config = self.platform_configs.get(platform_key, self.platform_configs['linux'])
        python_cmd = config['python_cmd']
        
        # 检查Python
        try:
            result = subprocess.run([python_cmd, '--version'], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"✅ Python环境: {result.stdout.strip()}")
            else:
                print(f"❌ Python检查失败")
                return False
        except FileNotFoundError:
            print(f"❌ {python_cmd} 未找到")
            return False
        
        # 检查tkinter（Linux特别需要）
        if target_platform == 'linux':
            try:
                result = subprocess.run([python_cmd, '-c', 'import tkinter'], 
                                      capture_output=True, text=True)
                if result.returncode == 0:
                    print("✅ tkinter支持检查通过")
                else:
                    print("❌ tkinter未安装，请安装python3-tk包")
                    return False
            except:
                print("❌ tkinter检查失败")
                return False
        
        # 检查PyInstaller
        try:
            result = subprocess.run([python_cmd, '-c', 'import PyInstaller'], 
                                  capture_output=True, text=True)
            if result.returncode != 0:
                print("📦 正在安装PyInstaller...")
                install_result = subprocess.run([python_cmd, '-m', 'pip', 'install', 'pyinstaller'])
                if install_result.returncode != 0:
                    print("❌ PyInstaller安装失败")
                    return False
            print("✅ PyInstaller准备就绪")
        except:
            print("❌ PyInstaller检查失败")
            return False
            
        return True
    
    def build_platform(self, target_platform):
        """构建指定平台的配置助手"""
        print(f"\n🚀 构建配置助手 {target_platform.upper()} 版本...")
        print("=" * 50)
        
        # 检查环境
        if not self.check_environment(target_platform):
            print(f"❌ {target_platform} 环境检查失败")
            return False
        
        # 获取平台配置
        platform_key = 'darwin' if target_platform == 'macos' else target_platform
        config = self.platform_configs.get(platform_key, self.platform_configs['linux'])
        
        # 清理旧文件
        self.cleanup_old_files(config['output_name'])
        
        # 构建PyInstaller命令
        cmd = [
            config['python_cmd'], '-m', 'PyInstaller',
            '--onefile',
            '--name', '配置助手',
            '--clean',
            '--noconfirm',
            '--hidden-import', 'tkinter',
            '--hidden-import', 'tkinter.messagebox',
            '--hidden-import', 'tkinter.scrolledtext',
            '--hidden-import', 'tkinter.simpledialog',
            '--hidden-import', 'tkinter.ttk',
            '--hidden-import', 'tkinter.filedialog',
            '--hidden-import', 'tkinter.colorchooser',
            '--hidden-import', 'tkinter.commondialog',
            '--collect-submodules', 'tkinter'
        ] + config['pyinstaller_args'] + [
            str(self.build_dir / 'config_helper.py')
        ]
        
        print("🔨 开始打包配置助手...")
        print(f"命令: {' '.join(cmd)}")
        
        # 执行构建
        result = subprocess.run(cmd, cwd=str(self.build_dir))
        
        if result.returncode == 0:
            return self.post_build_process(target_platform, config)
        else:
            print("❌ 构建失败")
            return False
    
    def cleanup_old_files(self, output_name):
        """清理旧的构建文件"""
        dist_dir = self.build_dir / 'dist'
        build_dir = self.build_dir / 'build'
        
        # 清理dist目录中的旧文件
        if dist_dir.exists():
            for file in dist_dir.glob('配置助手*'):
                if file.is_file():
                    file.unlink()
                elif file.is_dir():
                    shutil.rmtree(file)
        
        # 清理build目录
        config_build_dir = build_dir / '配置助手'
        if config_build_dir.exists():
            shutil.rmtree(config_build_dir)
    
    def post_build_process(self, target_platform, config):
        """构建后处理"""
        dist_dir = self.build_dir / 'dist'
        
        # 查找生成的文件
        possible_outputs = [
            dist_dir / '配置助手',
            dist_dir / '配置助手.exe',
            dist_dir / '配置助手.app'
        ]
        
        output_file = None
        for file in possible_outputs:
            if file.exists():
                output_file = file
                break
        
        if not output_file:
            print("❌ 找不到生成的可执行文件")
            return False
        
        print(f"✅ 配置助手构建成功！")
        print(f"📁 输出文件: {output_file}")
        
        # 获取文件大小
        if output_file.is_file():
            size = output_file.stat().st_size
            size_mb = size / (1024 * 1024)
            print(f"📏 文件大小: {size:,} 字节 ({size_mb:.1f} MB)")
        elif output_file.is_dir():
            # macOS .app包
            result = subprocess.run(['du', '-sh', str(output_file)], 
                                  capture_output=True, text=True)
            if result.returncode == 0:
                print(f"📏 应用大小: {result.stdout.split()[0]}")
        
        # 设置执行权限（Unix系统）
        if target_platform in ['macos', 'linux'] and output_file.is_file():
            os.chmod(output_file, 0o755)
            print("🔐 已设置执行权限")
        
        # 显示使用说明
        self.show_usage_instructions(target_platform, output_file)
        
        return True
    
    def show_usage_instructions(self, target_platform, output_file):
        """显示使用说明"""
        print("\n💡 使用说明:")
        
        if target_platform == 'windows':
            print("   双击运行 配置助手.exe")
        elif target_platform == 'macos':
            if output_file.suffix == '.app':
                print("   双击运行 配置助手.app")
            else:
                print("   在终端运行: ./dist/配置助手")
                print("   或双击文件管理器中的可执行文件")
        else:  # linux
            print("   在终端运行: ./dist/配置助手")
            print("   或双击文件管理器中的可执行文件")
            print("   注意: 需要GUI环境（X11显示服务器）")
        
        print("   然后:")
        print("   1. 输入墨问API密钥")
        print("   2. 点击'生成配置'按钮")
        print("   3. 复制生成的配置到Cursor等客户端")
        
        if target_platform == 'linux':
            print("\n📋 系统要求:")
            print("   - 需要X11显示服务器（桌面环境）")
            print("   - 如果在服务器环境，需要配置X11转发")
            print("   - 确保安装了python3-tk包")
    
    def build_all_platforms(self):
        """构建所有支持的平台"""
        print("🌍 开始跨平台构建配置助手...")
        
        platforms = ['windows', 'macos', 'linux']
        success_count = 0
        
        for platform_name in platforms:
            if self.build_platform(platform_name):
                success_count += 1
            print()  # 空行分隔
        
        print(f"🏁 构建完成！成功: {success_count}/{len(platforms)}")
        return success_count == len(platforms)
    
    def build_current_platform(self):
        """构建当前平台版本"""
        if self.current_platform == 'windows':
            return self.build_platform('windows')
        elif self.current_platform == 'darwin':
            return self.build_platform('macos')
        elif self.current_platform == 'linux':
            return self.build_platform('linux')
        else:
            print(f"⚠️ 当前平台 {self.current_platform} 可能不完全支持")
            return self.build_platform('linux')  # 默认使用linux配置

def main():
    """主函数"""
    parser = argparse.ArgumentParser(description='配置助手跨平台构建脚本')
    parser.add_argument('--platform', 
                       choices=['windows', 'macos', 'linux', 'all', 'current'],
                       default='current',
                       help='目标平台 (默认: current)')
    
    args = parser.parse_args()
    
    builder = ConfigHelperBuilder()
    
    if args.platform == 'all':
        success = builder.build_all_platforms()
    elif args.platform == 'current':
        success = builder.build_current_platform()
    else:
        success = builder.build_platform(args.platform)
    
    if success:
        print("\n🎉 构建成功！")
        sys.exit(0)
    else:
        print("\n❌ 构建失败！")
        sys.exit(1)

if __name__ == "__main__":
    main()