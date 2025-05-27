# 墨问笔记 MCP 服务器

这是一个基于**模型上下文协议（MCP）**的服务器，用于与墨问笔记软件进行交互。通过此服务器，你可以在支持MCP的应用（如Cursor、Claude Desktop等）中直接创建、编辑和管理墨问笔记。

## 功能特性

- 🔗 **兼容MCP协议**：支持最新的MCP 1.9.1版本
- 📝 **创建笔记**：支持创建简单文本笔记和富文本笔记
- ✏️ **编辑笔记**：支持编辑简单文本笔记和富文本笔记
- 🔒 **隐私设置**：设置笔记的公开、私有或规则公开权限
- 🔄 **密钥管理**：重置API密钥功能
- 🎨 **富文本支持**：支持加粗、高亮、链接等格式

## 快速开始

### 前提条件

- Python 3.8+
- 墨问Pro会员账号（API功能仅对Pro会员开放）
- 墨问API密钥（在墨问小程序中获取）

### 安装方式

#### 方式一：从源码安装（推荐）

1. **克隆项目**：
```bash
git clone https://github.com/z4656207/mowen-mcp-server.git
cd mowen-mcp-server
```

2. **安装依赖**：
```bash
pip install -e .
```

#### 方式二：直接安装依赖

```bash
pip install mcp httpx pydantic
```

### 配置 API 密钥

#### Windows PowerShell
```powershell
$env:MOWEN_API_KEY="你的墨问API密钥"
```

#### Linux/macOS
```bash
export MOWEN_API_KEY="你的墨问API密钥"
```

#### 持久化设置
创建 `.env` 文件：
```
MOWEN_API_KEY=你的墨问API密钥
```

### 配置 MCP 客户端

#### 方式一：模块安装方式（推荐）

如果你使用了 `pip install -e .` 安装，在 Cursor 设置中添加：

```json
{
  "mcp.servers": {
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

#### 方式二：直接文件路径方式

如果你没有安装包，可以直接指定文件路径：

```json
{
  "mcp.servers": {
    "mowen-mcp-server": {
      "command": "python",
      "args": ["绝对路径/mowen-mcp-server/src/mowen_mcp_server/server.py"],
      "env": {
        "MOWEN_API_KEY": "${env:MOWEN_API_KEY}"
      }
    }
  }
}
```

**注意**: 请将 `绝对路径` 替换为你的实际项目路径，例如：
- Windows: `"D:/CODE/mowen-mcp-server/src/mowen_mcp_server/server.py"`
- macOS/Linux: `"/home/user/mowen-mcp-server/src/mowen_mcp_server/server.py"`

## 可用工具

### create_note
创建一篇新的墨问笔记

**参数：**
- `content` (字符串)：笔记的文本内容
- `auto_publish` (布尔值，可选)：是否自动发布，默认为false
- `tags` (字符串数组，可选)：笔记标签列表

### create_rich_note
创建富文本笔记，支持格式化

**参数：**
- `paragraphs` (数组)：段落列表，支持加粗、高亮、链接等格式
- `auto_publish` (布尔值，可选)：是否自动发布
- `tags` (字符串数组，可选)：笔记标签列表

### edit_note
编辑已存在的笔记内容

**参数：**
- `note_id` (字符串)：要编辑的笔记ID
- `content` (字符串)：新的笔记内容

### edit_rich_note
编辑已存在的笔记为富文本格式

**参数：**
- `note_id` (字符串)：要编辑的笔记ID
- `paragraphs` (数组)：段落列表，支持加粗、高亮、链接等格式

**注意：** 此操作会完全替换笔记的原有内容，而不是追加内容

### set_note_privacy
设置笔记的隐私权限

**参数：**
- `note_id` (字符串)：笔记ID
- `privacy_type` (字符串)：隐私类型（public/private/rule）
- `no_share` (布尔值，可选)：是否禁止分享（仅rule类型有效）
- `expire_at` (整数，可选)：过期时间戳（仅rule类型有效，0表示永不过期）

### reset_api_key
重置墨问API密钥

**注意：** 此操作会使当前密钥立即失效

## API配额限制

根据墨问API文档，各接口有以下限制：

| API  | 配额       | 频率限制 | 说明                                      |
| ---- | -------- | ------ | --------------------------------------- |
| 笔记创建 | 100 次/天  | 1次/秒  | 调用成功才计为 1 次，**即：每天可以基于 API 创建 100 篇笔记** |
| 笔记编辑 | 1000 次/天 | 1次/秒  | 调用成功才计为 1 次，**即：每天可以基于 API 编辑 1000 次**  |
| 笔记设置 | 100 次/天  | 1次/秒  | 调用成功才计为 1 次                             |

## 项目结构

```
mowen-mcp-server/
├── src/
│   └── mowen_mcp_server/
│       ├── __init__.py       # 包初始化
│       ├── server.py         # MCP服务器主程序
│       └── config.py         # 配置管理
├── pyproject.toml            # 项目配置
├── README.md                 # 项目文档
└── 墨问API.md               # 墨问API详细文档
```

## 相关文档

- **墨问 API 在线文档**: [https://mowen.apifox.cn/](https://mowen.apifox.cn/)
- **本地API文档**: 详细的墨问API文档请参考项目中的 `墨问API.md` 文件
- **MCP协议文档**: [Model Context Protocol](https://modelcontextprotocol.io/)

## 常见问题

### Q: 为什么模块方式运行不起来？
A: 请确保使用 `pip install -e .` 安装了包，或者使用直接文件路径的配置方式。

### Q: API密钥在哪里获取？
A: 登录墨问小程序，在设置中找到API密钥管理，需要Pro会员权限。

### Q: 能编辑小程序创建的笔记吗？
A: 目前不支持，只能编辑通过API创建的笔记。

## 开发贡献

欢迎提交Issue和Pull Request！

### 开发环境设置

1. 克隆项目
2. 安装开发依赖：`pip install -e .`
3. 设置API密钥环境变量
4. 运行测试

## 许可证

本项目采用MIT许可证。详见 [LICENSE](LICENSE) 文件。

## 免责声明

本项目为个人开发的第三方工具，与墨问官方无关。使用前请确保遵守墨问的服务条款。 