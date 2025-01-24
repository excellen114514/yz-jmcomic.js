@echo off
chcp 65001 >nul
:loop
cls
echo 正在运行 Python 脚本...
python app.py
if %ERRORLEVEL% neq 0 (
    echo Python 脚本崩溃，正在重新启动...
    timeout /t 5
    goto loop
) else (
    echo Python 脚本正常退出。
)