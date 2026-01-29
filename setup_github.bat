@echo off
REM GitHub 自動上傳腳本 - Jeff命理世界 v6.7.1
REM 此腳本自動化 Git 操作流程

echo.
echo ╔════════════════════════════════════════════════════════════════╗
echo ║                                                                ║
echo ║         Jeff命理世界 - GitHub 自動上傳腳本                    ║
echo ║                                                                ║
echo ╚════════════════════════════════════════════════════════════════╝
echo.

setlocal enabledelayedexpansion

REM 檢查 Git 是否安裝
echo 檢查 Git 環境...
git --version >nul 2>&1
if errorlevel 1 (
    echo ❌ Git 未安裝或不在 PATH 中
    echo 請先安裝 Git: https://git-scm.com/download/win
    pause
    exit /b 1
)
echo ✅ Git 已就位

echo.
echo ════════════════════════════════════════════════════════════════
echo 第 1 步: 設定 Git 帳戶信息
echo ════════════════════════════════════════════════════════════════
echo.
echo 請輸入您的 GitHub 用戶名 (例如: yourusername):
set /p github_username="> "

echo.
echo 請輸入您的 GitHub 郵箱 (例如: your@email.com):
set /p github_email="> "

echo.
echo 正在配置 Git...
git config --global user.name "%github_username%"
git config --global user.email "%github_email%"
echo ✅ Git 帳戶已配置

echo.
echo ════════════════════════════════════════════════════════════════
echo 第 2 步: 初始化 Git 倉庫
echo ════════════════════════════════════════════════════════════════
echo.

REM 檢查是否已是 git 倉庫
if exist ".git" (
    echo ✅ 已是 Git 倉庫
) else (
    echo 初始化新的 Git 倉庫...
    git init
    echo ✅ Git 倉庫已初始化
)

echo.
echo ════════════════════════════════════════════════════════════════
echo 第 3 步: 添加所有文件到暫存區
echo ════════════════════════════════════════════════════════════════
echo.

git add .
echo ✅ 所有文件已添加

echo.
echo ════════════════════════════════════════════════════════════════
echo 第 4 步: 建立初始提交
echo ════════════════════════════════════════════════════════════════
echo.

git commit -m "Initial commit - Jeff命理世界 v6.7.1"
echo ✅ 初始提交已建立

echo.
echo ════════════════════════════════════════════════════════════════
echo 第 5 步: 建立版本標籤
echo ════════════════════════════════════════════════════════════════
echo.

git tag v6.7.1
echo ✅ 版本標籤 v6.7.1 已建立

echo.
echo ════════════════════════════════════════════════════════════════
echo 準備就緒！
echo ════════════════════════════════════════════════════════════════
echo.
echo 📋 後續步驟:
echo.
echo 1. 在 GitHub 建立新倉庫
echo    https://github.com/new
echo    倉庫名稱: JeffMingliShiJie
echo    請勿初始化任何檔案
echo.
echo 2. 執行以下命令推送代碼:
echo.
echo    git remote add origin https://github.com/YOUR_USERNAME/JeffMingliShiJie.git
echo    git branch -M main
echo    git push -u origin main
echo    git push origin v6.7.1
echo.
echo 3. GitHub Actions 會自動開始編譯！
echo    監控進度: https://github.com/YOUR_USERNAME/JeffMingliShiJie/actions
echo.
echo 按 Enter 鍵繼續...
pause

echo.
echo 💡 提示: 替換 YOUR_USERNAME 為您的 GitHub 用戶名
echo.
echo ════════════════════════════════════════════════════════════════
echo 🎉 本地 Git 設置完成！
echo ════════════════════════════════════════════════════════════════
