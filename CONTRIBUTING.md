# 贡献指南

感谢您对肺结核耐药性预测系统的关注！我们欢迎各种形式的贡献。

## 🤝 如何贡献

### 报告问题

如果您发现了bug或有功能建议，请：

1. 检查[Issues](../../issues)确保问题未被报告
2. 创建新的Issue，包含：
   - 清晰的问题描述
   - 重现步骤（如果是bug）
   - 期望的行为
   - 系统环境信息
   - 相关截图（如果适用）

### 提交代码

1. **Fork项目**
   ```bash
   git clone https://github.com/your-username/tuberculosis-prediction.git
   cd tuberculosis-prediction
   ```

2. **创建功能分支**
   ```bash
   git checkout -b feature/your-feature-name
   ```

3. **进行开发**
   - 遵循现有代码风格
   - 添加必要的测试
   - 更新相关文档

4. **提交更改**
   ```bash
   git add .
   git commit -m "feat: 添加新功能描述"
   ```

5. **推送分支**
   ```bash
   git push origin feature/your-feature-name
   ```

6. **创建Pull Request**
   - 提供清晰的PR描述
   - 关联相关Issues
   - 等待代码审查

## 📝 代码规范

### Python代码
- 遵循PEP 8规范
- 使用有意义的变量和函数名
- 添加适当的注释和文档字符串
- 保持函数简洁，单一职责

### 前端代码
- 使用一致的缩进（2个空格）
- 遵循语义化HTML
- CSS类名使用kebab-case
- JavaScript使用camelCase

### 提交信息规范

使用约定式提交格式：

```
<类型>(<范围>): <描述>

[可选的正文]

[可选的脚注]
```

**类型：**
- `feat`: 新功能
- `fix`: 错误修复
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建过程或辅助工具的变动

**示例：**
```
feat(prediction): 添加多语言支持

- 实现中英文界面切换
- 更新所有UI文本的国际化
- 添加语言选择器组件

Closes #123
```

## 🧪 测试

在提交代码前，请确保：

1. **运行现有测试**
   ```bash
   python -m pytest tests/
   ```

2. **添加新测试**
   - 为新功能编写单元测试
   - 确保测试覆盖率不降低

3. **手动测试**
   - 在本地环境测试所有功能
   - 验证UI在不同浏览器中的表现
   - 测试响应式设计

## 📋 开发环境设置

1. **克隆项目**
   ```bash
   git clone https://github.com/your-username/tuberculosis-prediction.git
   cd tuberculosis-prediction
   ```

2. **创建虚拟环境**
   ```bash
   python -m venv venv
   source venv/bin/activate  # Linux/macOS
   # 或
   venv\Scripts\activate     # Windows
   ```

3. **安装依赖**
   ```bash
   pip install -r requirements.txt
   ```

4. **启动开发服务器**
   ```bash
   export FLASK_ENV=development
   python app.py
   ```

## 🔍 代码审查

所有Pull Request都需要经过代码审查：

- 至少一位维护者的批准
- 通过所有自动化测试
- 符合项目的代码规范
- 包含适当的文档更新

## 📞 联系方式

如有疑问，可以通过以下方式联系：

- 创建GitHub Issue
- 发送邮件至项目维护者
- 参与项目讨论

## 📄 许可证

通过贡献代码，您同意您的贡献将在MIT许可证下发布。

---

再次感谢您的贡献！🎉