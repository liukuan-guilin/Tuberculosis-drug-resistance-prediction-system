# 肺结核耐药性预测系统

基于机器学习的肺结核耐药性智能预测Web应用，集成SHAP可解释性分析。

## 🌟 系统特点

- **智能预测**：基于随机森林模型，准确预测肺结核耐药性
- **可解释性**：集成SHAP分析，提供特征贡献度解释
- **用户友好**：现代化Web界面，操作简单直观
- **实时分析**：输入患者信息即可获得即时预测结果
- **专业可靠**：基于真实临床数据训练的高性能模型

## 📋 系统要求

- Python 3.8+
- 现代Web浏览器（Chrome、Firefox、Safari、Edge）
- 至少2GB可用内存

## 🚀 快速开始

### 1. 环境准备

```bash
# 创建虚拟环境（推荐）
python -m venv tb_prediction_env

# 激活虚拟环境
# Windows:
tb_prediction_env\Scripts\activate
# macOS/Linux:
source tb_prediction_env/bin/activate
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 启动系统

```bash
python app.py
```

### 4. 访问系统

打开浏览器访问：`http://localhost:5000`

## 📊 使用说明

### 输入参数说明

| 参数 | 说明 | 取值范围 |
|------|------|----------|
| 症状出现到诊断间隔天数 | 从症状出现到确诊的天数 | 0-365天 |
| 吸烟史 | 患者是否有吸烟史 | 否/是 |
| 结核病治疗史 | 患者的治疗历史 | 新发病例/既往治疗 |
| 治疗依从性 | 患者治疗配合程度 | 差/好 |
| 治疗前涂片结果 | 治疗前痰涂片检查结果 | 阴性/1+/2+/3+/4+ |
| 单核细胞计数 | 血液中单核细胞数量 | 0-2.0 (10^9/L) |
| 血红蛋白 | 血红蛋白浓度 | 50-200 (g/L) |
| 空腹血糖 | 空腹状态下血糖水平 | 3.0-20.0 (mmol/L) |
| 肺微结节 | 肺部是否存在微结节 | 否/是 |
| 肺空洞 | 肺部是否存在空洞 | 否/是 |
| 肺实变 | 肺部是否存在实变 | 否/是 |
| 预后营养指数 | 营养状况评估指标 | 20-70 |

### 结果解读

- **预测结果**：显示患者的耐药风险等级（高风险/低风险）
- **概率分布**：显示敏感和耐药的具体概率
- **特征贡献**：列出对预测结果影响最大的因素
- **SHAP值**：正值增加耐药风险，负值降低耐药风险

## 🔧 技术架构

### 后端技术
- **Flask**：Web框架
- **scikit-learn**：机器学习模型
- **SHAP**：模型可解释性分析
- **pandas/numpy**：数据处理

### 前端技术
- **Bootstrap 5**：响应式UI框架
- **Chart.js**：数据可视化
- **Font Awesome**：图标库
- **原生JavaScript**：交互逻辑

### 模型信息
- **算法**：随机森林（Random Forest）
- **特征数量**：12个核心临床特征
- **训练数据**：基于真实临床数据集
- **性能指标**：具有良好的准确性和泛化能力

## 📁 文件结构

```
肺结核耐药性预测系统/
├── app.py                              # 主应用程序
├── requirements.txt                    # Python依赖包
├── README.md                          # 说明文档
├── templates/
│   └── index.html                     # 前端页面模板
├── top1_model_随机森林.pkl             # 训练好的模型
├── scaler.pkl                         # 数据标准化器
├── feature_names.pkl                  # 特征名称列表
└── shap_feature_importance_top1_随机森林.csv  # 特征重要性数据
```

## ⚠️ 重要说明

1. **医疗免责声明**：本系统仅供医疗辅助参考，不能替代专业医生的诊断和治疗建议。

2. **数据隐私**：系统不会存储任何患者输入的数据，所有计算都在本地完成。

3. **模型局限性**：预测结果基于训练数据的统计模式，可能存在一定误差。

4. **使用建议**：建议结合临床经验和其他检查结果综合判断。

## 🛠️ 开发和部署

### 本地开发

```bash
# 开发模式启动（自动重载）
export FLASK_ENV=development  # Linux/macOS
set FLASK_ENV=development     # Windows
python app.py
```

### 生产部署

推荐使用Gunicorn部署：

```bash
# 安装Gunicorn
pip install gunicorn

# 启动生产服务器
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Docker部署

```dockerfile
# Dockerfile示例
FROM python:3.9-slim
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
EXPOSE 5000
CMD ["python", "app.py"]
```

## 📞 技术支持

如有技术问题或建议，请通过以下方式联系：

- 创建GitHub Issue
- 发送邮件至技术支持团队

## 📄 许可证

本项目仅供学术研究和教育用途使用。

---

**版本**：v1.0.0  
**更新时间**：2025年8月20日  
**开发团队**：桂林医科大呼吸病实验室-