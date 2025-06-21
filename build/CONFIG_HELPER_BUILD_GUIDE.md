 # 配置助手构建指南

## 概述

配置助手是一个图形化工具，帮助用户轻松生成墨问MCP服务器的配置文件。本指南说明如何在不同平台上构建配置助手。

## 支持的平台

- ✅ **Windows** - 生成 `.exe` 可执行文件
- ✅ **macOS** - 生成 `.app` 应用包或可执行文件
- ✅ **Linux** - 生成可执行文件

## 构建方法

### 方法一：使用Python脚本（推荐）

这是最灵活的构建方式，支持跨平台构建：

```bash
# 构建当前平台版本
python build_config_helper.py

# 构建指定平台版本
python build_config_helper.py --platform windows
python build_config_helper.py --platform macos
python build_config_helper.py --platform linux

# 构建所有平台版本
python build_config_helper.py --platform all
```

### 方法二：使用平台特定脚本

#### Windows
```cmd
# 方式1: 使用批处理脚本
build_config_helper_windows.bat

# 方式2: 直接使用PyInstaller
pyinstaller --onefile --windowed --name "配置助手" --clean --noconfirm config_helper.py
```

#### macOS
```bash
# 方式1: 使用Shell脚本
bash build_config_helper_macos.sh

# 方式2: 直接使用PyInstaller
pyinstaller --onefile --windowed --name "配置助手" --clean --noconfirm config_helper.py
```

#### Linux
```bash
# 方式1: 使用Shell脚本
bash build_config_helper_linux.sh

# 方式2: 直接使用PyInstaller
pyinstaller --onefile --windowed --name "配置助手" --clean --noconfirm config_helper.py
```

## 环境要求

### 通用要求
- Python 3.8 或更高版本
- pip 包管理器

### 平台特定要求

#### Windows
- 无额外要求

#### macOS
- 推荐使用 Homebrew 安装 Python
- 命令：`brew install python`

#### Linux
- 需要安装 tkinter 支持：
  - **Ubuntu/Debian**: `sudo apt install python3-tk`
  - **CentOS/RHEL**: `sudo yum install tkinter`
  - **Arch Linux**: tkinter 包含在 python 包中
- 需要GUI环境（X11显示服务器）

## 构建输出

构建成功后，可执行文件将生成在 `dist/` 目录中：

- **Windows**: `dist/配置助手.exe`
- **macOS**: `dist/配置助手` 或 `dist/配置助手.app`
- **Linux**: `dist/配置助手`

## 使用说明

### 运行配置助手

#### Windows
双击 `配置助手.exe` 运行

#### macOS
- 如果生成了 `.app` 文件：双击运行
- 如果是普通可执行文件：在终端运行 `./dist/配置助手`

#### Linux
- 终端运行：`./dist/配置助手`
- 或在文件管理器中双击可执行文件

### 配置步骤

1. **启动配置助手**
2. **输入API密钥**：在输入框中输入您的墨问API密钥
3. **生成配置**：点击"生成配置"按钮
4. **复制配置**：点击"复制到剪贴板"按钮
5. **应用配置**：将配置粘贴到Cursor或其他MCP客户端的设置中

## 故障排除

### 常见问题

#### 1. PyInstaller 未安装
**错误**: `ModuleNotFoundError: No module named 'PyInstaller'`

**解决方案**:
```bash
pip install pyinstaller
```

#### 2. tkinter 未安装 (Linux)
**错误**: `ModuleNotFoundError: No module named 'tkinter'`

**解决方案**:
```bash
# Ubuntu/Debian
sudo apt install python3-tk

# CentOS/RHEL
sudo yum install tkinter

# Arch Linux
# tkinter 已包含在 python 包中
```

#### 3. 权限问题 (macOS/Linux)
**错误**: 可执行文件无法运行

**解决方案**:
```bash
chmod +x dist/配置助手
```

#### 4. GUI 无法显示 (Linux服务器)
**错误**: `_tkinter.TclError: no display name and no $DISPLAY environment variable`

**解决方案**:
- 确保在桌面环境中运行
- 或配置X11转发：`ssh -X username@server`

### 构建失败处理

#### 1. 清理构建缓存
```bash
# 删除构建缓存
rm -rf build/ dist/
```

#### 2. 重新安装依赖
```bash
pip uninstall pyinstaller
pip install pyinstaller
```

#### 3. 检查Python版本
```bash
python --version
# 确保版本 >= 3.8
```

## 高级配置

### 自定义构建参数

如果需要自定义构建参数，可以直接使用PyInstaller：

```bash
pyinstaller \
    --onefile \
    --windowed \
    --name "配置助手" \
    --icon=icon.ico \
    --add-data "resources:resources" \
    --clean \
    --noconfirm \
    config_helper.py
```

### 添加图标

1. 准备图标文件（Windows: `.ico`, macOS: `.icns`, Linux: `.png`）
2. 在PyInstaller命令中添加 `--icon=path/to/icon`

### 包含额外资源

如果需要包含额外的资源文件：
```bash
--add-data "source:destination"
```

## 分发建议

### 文件组织
```
config-helper-release/
├── 配置助手(.exe/.app)     # 主程序
├── README.txt             # 使用说明
├── 使用指南.pdf           # 详细指南
└── 示例配置.json          # 配置示例
```

### 版本管理
- 在文件名中包含版本号：`配置助手-v1.0.0.exe`
- 维护版本更新日志
- 提供升级指南

### 安全考虑
- 建议对可执行文件进行数字签名
- 提供文件哈希值用于完整性验证
- 在官方渠道分发

## 开发者说明

### 源码结构
```python
class ConfigHelper:
    def __init__(self):
        # 初始化GUI和平台检测
        
    def setup_ui(self):
        # 设置用户界面
        
    def generate_config(self):
        # 生成MCP配置
        
    def copy_config(self):
        # 复制到剪贴板
        
    def save_config(self):
        # 保存到文件
```

### 平台适配
- 自动检测运行平台
- 适配不同平台的路径格式
- 处理平台特定的UI差异

### 扩展功能
- 支持配置验证
- 支持多种配置格式
- 支持配置模板

## 总结

配置助手的构建系统提供了多种构建方式，满足不同用户的需求：

- **开发者**：使用Python脚本进行灵活构建
- **运维人员**：使用平台脚本进行批量构建
- **普通用户**：直接下载预构建版本

通过这套构建系统，可以为不同平台的用户提供一致、易用的配置体验。