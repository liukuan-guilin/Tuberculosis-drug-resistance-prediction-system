@echo off
chcp 65001
echo ========================================
echo    肺结核耐药性预测系统启动脚本
echo ========================================
echo.

echo 正在检查Python环境...
python --version >nul 2>&1
if errorlevel 1 (
    echo 错误：未找到Python环境，请先安装Python 3.8+
    pause
    exit /b 1
)

echo ✓ Python环境检查通过
echo.

echo 正在检查依赖包...
pip show flask >nul 2>&1
if errorlevel 1 (
    echo 正在安装依赖包...
    pip install -r requirements.txt
    if errorlevel 1 (
        echo 错误：依赖包安装失败
        pause
        exit /b 1
    )
) else (
    echo ✓ 依赖包检查通过
)

echo.
echo 正在启动肺结核耐药性预测系统...
echo 请稍候...
echo.
echo ========================================
echo 系统启动后请访问: http://localhost:5000
echo 按 Ctrl+C 可停止服务
echo ========================================
echo.

python app.py

echo.
echo 系统已停止运行
pause