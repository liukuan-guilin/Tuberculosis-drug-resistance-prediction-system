#!/bin/bash

# 肺结核耐药性预测系统启动脚本

echo "========================================"
echo "    肺结核耐药性预测系统启动脚本"
echo "========================================"
echo

# 检查Python环境
echo "正在检查Python环境..."
if ! command -v python3 &> /dev/null; then
    if ! command -v python &> /dev/null; then
        echo "错误：未找到Python环境，请先安装Python 3.8+"
        exit 1
    else
        PYTHON_CMD="python"
    fi
else
    PYTHON_CMD="python3"
fi

echo "✓ Python环境检查通过"
echo

# 检查pip
echo "正在检查pip..."
if ! command -v pip3 &> /dev/null; then
    if ! command -v pip &> /dev/null; then
        echo "错误：未找到pip，请先安装pip"
        exit 1
    else
        PIP_CMD="pip"
    fi
else
    PIP_CMD="pip3"
fi

echo "✓ pip检查通过"
echo

# 检查依赖包
echo "正在检查依赖包..."
if ! $PYTHON_CMD -c "import flask" &> /dev/null; then
    echo "正在安装依赖包..."
    $PIP_CMD install -r requirements.txt
    if [ $? -ne 0 ]; then
        echo "错误：依赖包安装失败"
        exit 1
    fi
else
    echo "✓ 依赖包检查通过"
fi

echo
echo "正在启动肺结核耐药性预测系统..."
echo "请稍候..."
echo
echo "========================================"
echo "系统启动后请访问: http://localhost:5000"
echo "按 Ctrl+C 可停止服务"
echo "========================================"
echo

# 启动应用
$PYTHON_CMD app.py

echo
echo "系统已停止运行"