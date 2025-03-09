@echo off
setlocal

:: 设置 UTF-8 编码
chcp 65001 >nul

:: 设置 GitHub 仓库的 URL
set "GITHUB_REPO_URL=https://github.com/excellen114514/yz-jmcomic.js"

:: 设置要下载的文件列表
set "FILES=app.py .env requirements.txt option.yml"

:: 创建一个临时目录来克隆仓库
set "TEMP_DIR=temp_repo"
mkdir %TEMP_DIR%
cd %TEMP_DIR%

:: 克隆仓库（只克隆最新的一次提交，减少下载量）
echo 正在克隆仓库...
git clone --depth 1 %GITHUB_REPO_URL% .
if %errorlevel% neq 0 (
    echo 克隆仓库失败！
    cd ..
    rmdir /s /q %TEMP_DIR%
    endlocal
    pause
    exit /b
)

:: 遍历文件列表并复制到当前目录
for %%F in (%FILES%) do (
    if exist %%F (
        echo 正在复制 %%F ...
        copy %%F ..\
        echo %%F 下载成功！
    ) else (
        echo %%F 不存在于仓库中！
    )
)

:: 清理临时目录
cd ..
rmdir /s /q %TEMP_DIR%

endlocal
echo 所有文件下载完成！
pause