@echo off
chcp 65001 >nul
title Jeff命理世界 v6.7.3 Slim Fixed - 修正版
mode con cols=80 lines=35
color 0E

echo.
echo ╔════════════════════════════════════════════════════════════════════════╗
echo ║                                                                        ║
echo ║       Jeff命理世界 v6.7.3 Slim Fixed - 修正版 (19.36 MB)          ║
echo ║                                                                        ║
echo ║       修正：PIL 模組缺失問題已解決                                  ║
echo ║       優化：仍保持小於 20MB (比目標小 3%)                          ║
echo ║                                                                        ║
echo ╚════════════════════════════════════════════════════════════════════════╝
echo.
echo   [修正內容]
echo   ✓ 保留 PIL (Pillow) - 必需用於背景圖片
echo   ✓ 排除未使用大型庫 (matplotlib, numpy, pandas, cv2, scipy)
echo   ✓ 所有功能完整可用
echo.
echo   [版本比較]
echo   • 原瘦身版: 12.2 MB (缺少 PIL，無法執行)
echo   • 修正版:   19.36 MB (完整可用，低於 20MB 目標)
echo   • 完整版:   31.13 MB (所有庫完整)
echo.
echo   正在啟動程式...
echo.

"Jeff命理世界_v6.7.3_Slim_Fixed.exe"

if errorlevel 1 (
    echo.
    echo ❌ 程式執行失敗！錯誤代碼：%errorlevel%
    echo.
    pause
)
