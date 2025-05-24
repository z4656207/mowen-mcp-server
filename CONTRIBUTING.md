# 贡献指南

感谢您对墨问笔记 MCP 服务器项目的关注！我们欢迎所有形式的贡献。

## 如何贡献

### 报告问题

如果您发现了问题或有建议，请：

1. 查看 [Issues](https://github.com/z4656207/mowen-mcp-server/issues) 确保问题未被报告
2. 创建新的 Issue，包含以下信息：
   - 详细的问题描述
   - 复现步骤
   - 期望的行为
   - 实际的行为
   - 环境信息（操作系统、Python版本等）

### 提交代码

1. **Fork 项目**
   ```bash
   git clone https://github.com/z4656207/mowen-mcp-server.git
   cd mowen-mcp-server
   ```

2. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **安装开发依赖**
   ```bash
   pip install -e .
   ```

4. **进行更改**
   - 保持代码风格一致
   - 添加必要的注释
   - 更新相关文档

5. **测试更改**
   ```bash
   # 设置测试环境变量
   export MOWEN_API_KEY="your_test_api_key"
   
   # 运行基本测试
   python -m mowen_mcp_server.server
   ```

6. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

7. **推送并创建 Pull Request**
   ```bash
   git push origin feature/your-feature-name
   ```

## 代码规范

### Python 代码风格

- 遵循 [PEP 8](https://pep8.org/) 风格指南
- 使用有意义的变量和函数名
- 保持函数简洁，单一职责
- 添加类型注解

### 提交信息格式

使用语义化提交信息：

- `feat: 添加新功能`
- `fix: 修复问题`
- `docs: 更新文档`
- `style: 代码格式化`
- `refactor: 重构代码`
- `test: 添加测试`
- `chore: 构建或辅助工具修改`

### 文档要求

- 更新 README.md（如果适用）
- 在代码中添加docstring
- 更新 API 文档（如果适用）

## 开发环境设置

### 必需软件

- Python 3.8+
- Git
- 墨问Pro会员账号（用于测试）

### 环境变量

创建 `env.example` 的副本并重命名为 `.env`：

```bash
cp env.example .env
```

然后编辑 `.env` 文件，填入您的API密钥。

### 项目结构

```
mowen-mcp-server/
├── src/mowen_mcp_server/   # 主要源代码
├── tests/                  # 测试文件（待添加）
├── docs/                   # 文档（待添加）
├── pyproject.toml         # 项目配置
└── README.md              # 项目说明
```

## 发布流程

项目维护者将处理版本发布：

1. 更新版本号
2. 更新 CHANGELOG
3. 创建 GitHub Release
4. 发布到 PyPI（如果适用）

## 行为准则

- 尊重他人
- 保持友好和建设性的讨论
- 专注于技术问题
- 遵守开源社区的最佳实践

## 联系方式

如有疑问，请：

1. 创建 Issue
2. 发起 Discussion（如果启用）
3. 通过邮件联系维护者

## 许可证

通过贡献代码，您同意您的贡献将在 MIT 许可证下分发。 