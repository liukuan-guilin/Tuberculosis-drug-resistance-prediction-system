#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
测试预测功能
"""

import requests
import json

def test_prediction():
    """测试预测接口"""
    url = "http://localhost:5000/predict"
    
    # 测试数据
    test_data = {
        "Interval from Symptom Onset to Diagnosis (days)": 30,
        "Smoking History 0=No 1=Yes": "0",
        "Tuberculosis Treatment History 1=New Case 2=Previously treated": "1",
        "Treatment Adherence 0=Poor 1=Good": "1",
        "Pretreatment smear results 0=Negative 1=1+ 2=2+ 3=3+ 4=4+": "0",
        "Monocytes (10^9/L)": 0.5,
        "Hemoglobin (HGB, g/L)": 120,
        "FPG (mmol/L)": 5.5,
        "Pulmonary Micronodules 0=No 1=Yes": "0",
        "Pulmonary Cavitation 0=No 1=Yes": "0",
        "Pulmonary Consolidation 0=No 1=Yes": "0",
        "PNI": 45
    }
    
    try:
        print("发送预测请求...")
        print(f"请求数据: {json.dumps(test_data, indent=2, ensure_ascii=False)}")
        
        response = requests.post(url, json=test_data, timeout=30)
        
        print(f"响应状态码: {response.status_code}")
        print(f"响应内容: {response.text}")
        
        if response.status_code == 200:
            result = response.json()
            print("\n预测成功！")
            print(f"预测结果: {result.get('prediction')}")
            print(f"风险等级: {result.get('risk_level')}")
            print(f"概率: {result.get('probability')}")
            print(f"基准值: {result.get('base_value')}")
            print(f"重要特征数量: {len(result.get('top_features', []))}")
        else:
            print("\n预测失败！")
            try:
                error_info = response.json()
                print(f"错误信息: {error_info}")
            except:
                print(f"原始错误响应: {response.text}")
                
    except requests.exceptions.RequestException as e:
        print(f"请求异常: {e}")
    except Exception as e:
        print(f"其他异常: {e}")

if __name__ == "__main__":
    test_prediction()