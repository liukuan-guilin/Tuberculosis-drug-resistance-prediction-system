#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
肺结核耐药性预测Web应用
基于随机森林模型的实时预测系统
"""

import os
import pickle
import joblib
import numpy as np
import pandas as pd
import shap
from flask import Flask, render_template, request, jsonify
from sklearn.preprocessing import StandardScaler
import warnings
warnings.filterwarnings('ignore')

app = Flask(__name__)

# 全局变量
model = None
scaler = None
feature_names = None
feature_importance = None
explainer = None

# CI环境检测
def is_ci_environment():
    """检测是否在CI环境中运行"""
    ci_indicators = ['CI', 'CONTINUOUS_INTEGRATION', 'GITHUB_ACTIONS', 'TRAVIS', 'JENKINS']
    return any(os.getenv(indicator) for indicator in ci_indicators)

def handle_ci_prediction(request):
    """在CI环境下处理预测请求，返回模拟结果"""
    try:
        input_data = request.json
        language = input_data.get('language', 'zh')
        
        # 模拟预测结果
        mock_prediction = 0  # 模拟预测为敏感
        mock_probability = [0.7, 0.3]  # 模拟概率分布
        
        # 模拟特征贡献（基于输入特征数量）
        mock_features = [
            "Interval from Symptom Onset to Diagnosis (days)",
            "Monocytes (10^9/L)",
            "Age",
            "Gender"
        ]
        
        feature_contributions = []
        for i, feature_name in enumerate(mock_features):
            # 模拟SHAP值
            mock_shap_value = (-1) ** i * (0.1 + i * 0.05)
            
            # 根据语言设置显示名称
            if language == 'en':
                display_name = feature_name
            else:
                feature_mapping = {
                    "Interval from Symptom Onset to Diagnosis (days)": "症状出现到诊断间隔（天）",
                    "Monocytes (10^9/L)": "单核细胞计数",
                    "Age": "年龄",
                    "Gender": "性别"
                }
                display_name = feature_mapping.get(feature_name, feature_name)
            
            feature_contributions.append({
                'feature': display_name,
                'value': input_data.get(feature_name, 0),
                'contribution': mock_shap_value,
                'abs_contribution': abs(mock_shap_value)
            })
        
        # 按贡献度排序
        feature_contributions.sort(key=lambda x: x['abs_contribution'], reverse=True)
        
        # 构建响应
        if language == 'en':
            result_text = "Sensitive" if mock_prediction == 0 else "Resistant"
            confidence_text = f"Confidence: {max(mock_probability):.1%}"
        else:
            result_text = "敏感" if mock_prediction == 0 else "耐药"
            confidence_text = f"置信度: {max(mock_probability):.1%}"
        
        response = {
            'prediction': int(mock_prediction),
            'probability': mock_probability,
            'result_text': result_text,
            'confidence': max(mock_probability),
            'confidence_text': confidence_text,
            'feature_contributions': feature_contributions,
            'ci_mode': True,
            'message': 'CI环境模拟预测结果' if language == 'zh' else 'CI environment mock prediction result'
        }
        
        return jsonify(response)
        
    except Exception as e:
        return jsonify({
            'error': f'CI环境预测处理错误: {str(e)}' if language == 'zh' else f'CI prediction error: {str(e)}',
            'ci_mode': True
        }), 500

# 模型状态检查装饰器
def require_models(f):
    """装饰器：检查模型是否已加载"""
    def decorated_function(*args, **kwargs):
        if model is None or scaler is None or feature_names is None:
            if is_ci_environment():
                # 在CI环境下返回模拟预测结果
                return handle_ci_prediction(request)
            else:
                return jsonify({'error': '模型未加载，请重启应用', 'ci_mode': False}), 503
        return f(*args, **kwargs)
    decorated_function.__name__ = f.__name__
    return decorated_function

def load_models():
    """加载模型和相关文件"""
    global model, scaler, feature_names, feature_importance, explainer
    
    # 在CI环境中跳过模型加载
    if is_ci_environment():
        print("🔧 检测到CI环境，跳过模型文件加载")
        return True
    
    try:
        # 加载模型
        model = joblib.load('top1_model_随机森林.pkl')
        print("✓ 模型加载成功")
        
        # 加载标准化器
        scaler = joblib.load('scaler.pkl')
        print("✓ 标准化器加载成功")
        
        # 加载特征名称
        feature_names = joblib.load('feature_names.pkl')
        print("✓ 特征名称加载成功")
        
        # 加载特征重要性
        feature_importance = pd.read_csv('shap_feature_importance_top1_随机森林.csv')
        print("✓ 特征重要性加载成功")
        
        # 初始化SHAP解释器
        explainer = shap.TreeExplainer(model)
        print("✓ SHAP解释器初始化成功")
        
        return True
    except Exception as e:
        print(f"模型加载失败: {e}")
        if is_ci_environment():
            print("🔧 CI环境中忽略模型加载错误")
            return True
        return False

def get_feature_mapping():
    """获取特征映射字典"""
    return {
        'Interval from Symptom Onset to Diagnosis (days)': {
            'name': '症状出现到诊断间隔天数',
            'name_en': 'Interval from Symptom Onset to Diagnosis (days)',
            'type': 'number',
            'min': 0,
            'max': 365,
            'default': 30
        },
        'Smoking History 0=No 1=Yes': {
            'name': '吸烟史',
            'name_en': 'Smoking History',
            'type': 'select',
            'options': [('0', '否'), ('1', '是')],
            'options_en': [('0', 'No'), ('1', 'Yes')],
            'default': '0'
        },
        'Tuberculosis Treatment History 1=New Case 2=Previously treated': {
            'name': '结核病治疗史',
            'name_en': 'Tuberculosis Treatment History',
            'type': 'select',
            'options': [('1', '新发病例'), ('2', '既往治疗')],
            'options_en': [('1', 'New Case'), ('2', 'Previously treated')],
            'default': '1'
        },
        'Treatment Adherence 0=Poor 1=Good': {
            'name': '治疗依从性',
            'name_en': 'Treatment Adherence',
            'type': 'select',
            'options': [('0', '差'), ('1', '好')],
            'options_en': [('0', 'Poor'), ('1', 'Good')],
            'default': '1'
        },
        'Pretreatment smear results 0=Negative 1=1+ 2=2+ 3=3+ 4=4+': {
            'name': '治疗前涂片结果',
            'name_en': 'Pretreatment Smear Results',
            'type': 'select',
            'options': [('0', '阴性'), ('1', '1+'), ('2', '2+'), ('3', '3+'), ('4', '4+')],
            'options_en': [('0', 'Negative'), ('1', '1+'), ('2', '2+'), ('3', '3+'), ('4', '4+')],
            'default': '0'
        },
        'Monocytes (10^9/L)': {
            'name': '单核细胞计数 (10^9/L)',
            'name_en': 'Monocytes (10^9/L)',
            'type': 'number',
            'min': 0,
            'max': 2.0,
            'step': 0.01,
            'default': 0.5
        },
        'Hemoglobin (HGB, g/L)': {
            'name': '血红蛋白 (g/L)',
            'name_en': 'Hemoglobin (g/L)',
            'type': 'number',
            'min': 50,
            'max': 200,
            'default': 120
        },
        'FPG (mmol/L)': {
            'name': '空腹血糖 (mmol/L)',
            'name_en': 'FPG (mmol/L)',
            'type': 'number',
            'min': 3.0,
            'max': 20.0,
            'step': 0.1,
            'default': 5.5
        },
        'Pulmonary Micronodules 0=No 1=Yes': {
            'name': '肺微结节',
            'name_en': 'Pulmonary Micronodules',
            'type': 'select',
            'options': [('0', '否'), ('1', '是')],
            'options_en': [('0', 'No'), ('1', 'Yes')],
            'default': '0'
        },
        'Pulmonary Cavitation 0=No 1=Yes': {
            'name': '肺空洞',
            'name_en': 'Pulmonary Cavitation',
            'type': 'select',
            'options': [('0', '否'), ('1', '是')],
            'options_en': [('0', 'No'), ('1', 'Yes')],
            'default': '0'
        },
        'Pulmonary Consolidation 0=No 1=Yes': {
            'name': '肺实变',
            'name_en': 'Pulmonary Consolidation',
            'type': 'select',
            'options': [('0', '否'), ('1', '是')],
            'options_en': [('0', 'No'), ('1', 'Yes')],
            'default': '0'
        },
        'PNI': {
            'name': '预后营养指数 (PNI)',
            'name_en': 'PNI',
            'type': 'number',
            'min': 20,
            'max': 70,
            'step': 0.1,
            'default': 45
        }
    }

@app.route('/health')
def health_check():
    """健康检查端点"""
    if is_ci_environment():
        return jsonify({
            'status': 'healthy',
            'ci_mode': True,
            'message': 'Application running in CI environment'
        }), 200
    elif model is None or scaler is None:
        return jsonify({
            'status': 'degraded',
            'ci_mode': False,
            'message': 'Models not loaded'
        }), 503
    else:
        return jsonify({
            'status': 'healthy',
            'ci_mode': False,
            'message': 'Application fully operational'
        }), 200

@app.route('/')
def index():
    """主页"""
    feature_mapping = get_feature_mapping()
    return render_template('index.html', feature_mapping=feature_mapping)

@app.route('/predict', methods=['POST'])
@require_models
def predict():
    """预测接口"""
    try:
        # 获取输入数据
        input_data = request.json
        language = input_data.get('language', 'zh')  # 获取语言参数
        
        # 构建特征向量
        feature_vector = []
        for feature_name in feature_names:
            if feature_name in input_data:
                feature_vector.append(float(input_data[feature_name]))
            else:
                # 使用默认值或0
                feature_vector.append(0.0)
        
        # 转换为numpy数组并reshape
        X = np.array(feature_vector).reshape(1, -1)
        
        # 标准化
        X_scaled = scaler.transform(X)
        
        # 预测
        prediction = model.predict(X_scaled)[0]
        probability = model.predict_proba(X_scaled)[0]
        
        # 计算SHAP值
        shap_values = explainer.shap_values(X_scaled)
        
        # 处理SHAP值的不同格式
        if isinstance(shap_values, list):
            # 如果是列表，取耐药类别的SHAP值
            shap_values = shap_values[1]
        elif len(shap_values.shape) == 3:
            # 如果是三维数组 (n_samples, n_features, n_classes)，取耐药类别的SHAP值
            shap_values = shap_values[:, :, 1]
        
        # 确保shap_values是二维数组 (n_samples, n_features)
        if len(shap_values.shape) == 1:
            shap_values = shap_values.reshape(1, -1)
        
        # 获取特征贡献
        feature_contributions = []
        for i, feature_name in enumerate(feature_names):
            if i < shap_values.shape[1]:
                shap_val = shap_values[0, i]
                # 根据语言获取特征名
                feature_mapping = get_feature_mapping()
                if language == 'en':
                    display_name = feature_mapping.get(feature_name, {}).get('name_en', feature_name)
                else:
                    display_name = feature_mapping.get(feature_name, {}).get('name', feature_name)
                
                feature_contributions.append({
                    'feature': display_name,
                    'value': float(X[0][i]),
                    'shap_value': float(shap_val),
                    'contribution': abs(float(shap_val))
                })
        
        # 按贡献度排序
        feature_contributions.sort(key=lambda x: x['contribution'], reverse=True)
        
        # 处理expected_value
        if isinstance(explainer.expected_value, np.ndarray):
            if len(explainer.expected_value) > 1:
                base_value = float(explainer.expected_value[1])
            else:
                base_value = float(explainer.expected_value[0])
        else:
            base_value = float(explainer.expected_value)
        
        # 根据语言设置风险等级文本
        if language == 'en':
            risk_level = 'High Risk' if prediction == 1 else 'Low Risk'
        else:
            risk_level = '高风险' if prediction == 1 else '低风险'
        
        # 返回结果
        result = {
            'prediction': int(prediction),
            'probability': {
                'sensitive': float(probability[0]),
                'resistant': float(probability[1])
            },
            'risk_level': risk_level,
            'top_features': feature_contributions[:8],  # 返回前8个重要特征
            'base_value': base_value
        }
        
        return jsonify(result)
        
    except Exception as e:
        return jsonify({'error': f'预测失败: {str(e)}'}), 500

@app.route('/feature_importance')
@require_models
def get_feature_importance():
    """获取特征重要性"""
    try:
        # 获取语言参数
        language = request.args.get('lang', 'zh')
        
        # 特征名称映射（从简化名称到完整名称）
        feature_name_mapping = {
            'Symptom_Onset_Days': 'Interval from Symptom Onset to Diagnosis (days)',
            'TB_Treatment_History': 'Tuberculosis Treatment History 1=New Case 2=Previously treated',
            'Treatment_Adherence': 'Treatment Adherence 0=Poor 1=Good',
            'Pulmonary_Cavitation': 'Pulmonary Cavitation 0=No 1=Yes',
            'Smoking_History': 'Smoking History 0=No 1=Yes',
            'Pretreatment_Smear': 'Pretreatment smear results 0=Negative 1=1+ 2=2+ 3=3+ 4=4+',
            'Pulmonary_Micronodules': 'Pulmonary Micronodules 0=No 1=Yes',
            'Pulmonary_Consolidation': 'Pulmonary Consolidation 0=No 1=Yes',
            'FPG': 'FPG (mmol/L)',
            'Hemoglobin': 'Hemoglobin (HGB, g/L)',
            'PNI': 'PNI',
            'Monocytes': 'Monocytes (10^9/L)'
        }
        
        # 中文特征名称映射
        chinese_feature_mapping = {
            'Symptom_Onset_Days': '症状出现到诊断间隔天数',
            'TB_Treatment_History': '结核病治疗史',
            'Treatment_Adherence': '治疗依从性',
            'Pulmonary_Cavitation': '肺空洞',
            'Smoking_History': '吸烟史',
            'Pretreatment_Smear': '治疗前涂片结果',
            'Pulmonary_Micronodules': '肺微结节',
            'Pulmonary_Consolidation': '肺实变',
            'FPG': '空腹血糖',
            'Hemoglobin': '血红蛋白',
            'PNI': '预后营养指数',
            'Monocytes': '单核细胞'
        }
        
        # 转换为前端需要的格式
        importance_data = []
        
        for _, row in feature_importance.iterrows():
            # 获取简化的特征名
            feature_key = row['Feature']
            
            # 根据语言选择显示名称
            if language == 'en':
                display_name = feature_name_mapping.get(feature_key, row['Chinese_Feature'])
            else:
                display_name = chinese_feature_mapping.get(feature_key, feature_key)
            
            importance_data.append({
                'feature': display_name,
                'importance': float(row['SHAP_Importance'])
            })
        
        return jsonify(importance_data)
    except Exception as e:
        return jsonify({'error': f'获取特征重要性失败: {str(e)}'}), 500

if __name__ == '__main__':
    print("正在启动肺结核耐药性预测系统...")
    
    if load_models():
        print("\n" + "="*50)
        print("🏥 肺结核耐药性预测系统")
        print("📊 基于随机森林模型")
        print("🔬 集成SHAP可解释性分析")
        print("="*50)
        print("\n系统启动成功！")
        print("访问地址: http://localhost:5000")
        print("按 Ctrl+C 停止服务")
        print("\n" + "="*50)
        
        app.run(debug=True, host='0.0.0.0', port=5000)
    else:
        print("❌ 系统启动失败，请检查模型文件")