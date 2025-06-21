# 跨平台构建说明

## 支持的平台

- ✅ Windows (exe文件)
- ✅ macOS (app文件/可执行文件)
- ✅ Linux (可执行文件)

## 构建项目

### 1. 主程序构建

#### 方法一：使用Python脚本（推荐）

```bash
# 构建当前平台版本
python build_release.py

# 构建指定平台版本
python build_release.py --platform windows
python build_release.py --platform macos
python build_release.py --platform linux
```

#### 方法二：使用平台脚本

**Windows:**
```cmd
build_windows.bat
```

**macOS:**
```bash
bash build_macos.sh
```

**Linux:**
```bash
bash build_linux.sh
```

### 2. 配置助手构建

配置助手是一个独立的图形化工具，帮助用户生成MCP配置文件。

#### 方法一：使用Python脚本（推荐）

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

#### 方法二：使用平台脚本

**Windows:**
```cmd
build_config_helper_windows.bat
```

**macOS:**
```bash
bash build_config_helper_macos.sh
```

**Linux:**
```bash
bash build_config_helper_linux.sh
```

## 输出结构

### 主程序构建输出

构建完成后，`release/` 目录结构：

```
release/
├── windows-release/
│   ├── developer-version/          # 开发者版本（源码）
│   │   ├── src/
│   │   ├── scripts/
│   │   ├── pyproject.toml
│   │   └── INSTALL_GUIDE.md
│   └── user-version/               # 用户版本（可执行文件）
│       ├── mowen-mcp-server.exe
│       ├── 配置助手.exe
│       ├── USER_GUIDE.md
│       └── start_server.bat
├── macos-release/
│   ├── developer-version/
│   └── user-version/
│       ├── mowen-mcp-server
│       ├── 配置助手.app
│       ├── USER_GUIDE.md
│       └── start_server.sh
└── linux-release/
    ├── developer-version/
    └── user-version/
        ├── mowen-mcp-server
        ├── 配置助手
        ├── USER_GUIDE.md
        └── start_server.sh
```

### 配置助手构建输出

配置助手构建完成后，输出在 `build/dist/` 目录：

- **Windows**: `dist/配置助手.exe`
- **macOS**: `dist/配置助手` 或 `dist/配置助手.app`
- **Linux**: `dist/配置助手`

## 相关文档

- **构建技术说明**: [BUILD_TECHNICAL_GUIDE.md](BUILD_TECHNICAL_GUIDE.md) - 详细的技术架构和实现说明
- **配置助手构建指南**: [CONFIG_HELPER_BUILD_GUIDE.md](CONFIG_HELPER_BUILD_GUIDE.md) - 配置助手专门的构建说明

## 环境要求

### 通用要求
- Python 3.8 或更高版本
- pip 包管理器
- PyInstaller (自动安装)

### 平台特定要求

#### Linux 额外要求
- tkinter 支持: `sudo apt install python3-tk` (Ubuntu/Debian)
- GUI 环境 (X11显示服务器)

#### macOS 建议
- 使用 Homebrew 安装 Python: `brew install python`

## 快速开始

1. **克隆项目并进入构建目录**:
   ```bash
   git clone <repository>
   cd mowen-mcp-server/build
   ```

2. **构建主程序**:
   ```bash
   python build_release.py
   ```

3. **构建配置助手**:
   ```bash
   python build_config_helper.py
   ```

4. **查看构建结果**:
   - 主程序: `../release/[platform]-release/`
   - 配置助手: `dist/` 