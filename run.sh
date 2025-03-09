#!/bin/bash

# 设置 GitHub 仓库的 URL
GITHUB_REPO_URL="https://github.com/excellen114514/yz-jmcomic.js"

# 设置要下载的文件列表
FILES=("app.py" ".env" "requirements.txt" "option.yml")

# 创建一个临时目录来克隆仓库
TEMP_DIR="temp_repo"
mkdir -p "$TEMP_DIR"
cd "$TEMP_DIR" || exit

# 克隆仓库（只克隆最新的一次提交，减少下载量）
echo "正在克隆仓库..."
git clone --depth 1 "$GITHUB_REPO_URL" .
if [ $? -ne 0 ]; then
    echo "克隆仓库失败！"
    cd ..
    rm -rf "$TEMP_DIR"
    exit 1
fi

# 遍历文件列表并复制到当前目录
for FILE in "${FILES[@]}"; do
    if [ -f "$FILE" ]; then
        echo "正在复制 $FILE ..."
        cp "$FILE" ../
        echo "$FILE 下载成功！"
    else
        echo "$FILE 不存在于仓库中！"
    fi
done

# 清理临时目录
cd ..
rm -rf "$TEMP_DIR"

echo "所有文件下载完成！"