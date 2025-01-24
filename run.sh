#!/bin/bash

while true; do
    echo "正在运行 Python 脚本..."
    python app.py
    if [ $? -ne 0 ]; then
        echo "Python 脚本崩溃，正在重新启动..."
        sleep 5
    else
        echo "Python 脚本正常退出。"
        break
    fi
done