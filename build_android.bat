@echo off
REM Android App 編譯和部署腳本 (Windows PowerShell 版)

echo ======================================
echo Jeff命理世界 - Android APP 編譯腳本
echo ======================================

setlocal enabledelayedexpansion

REM 檢查環境變數
echo.
echo [1] 檢查環境變數...

if not defined ANDROID_SDK_ROOT (
    echo. ✗ ANDROID_SDK_ROOT 未設定
    echo 設定命令: set ANDROID_SDK_ROOT=C:\Users\[YourUsername]\AppData\Local\Android\Sdk
    pause
    exit /b 1
) else (
    echo ✓ ANDROID_SDK_ROOT: %ANDROID_SDK_ROOT%
)

if not defined JAVA_HOME (
    echo ✗ JAVA_HOME 未設定
    pause
    exit /b 1
) else (
    echo ✓ JAVA_HOME: %JAVA_HOME%
)

REM 檢查 Android SDK
echo.
echo [2] 檢查 Android SDK...

if exist "%ANDROID_SDK_ROOT%\platforms\android-31" (
    echo ✓ Android API 31 已安裝
) else (
    echo ✗ Android API 31 未安裝
    echo 請用 Android Studio SDK Manager 安裝
    pause
    exit /b 1
)

REM 進入專案目錄
cd /d "%~dp0"

REM 清潔舊檔案
echo.
echo [3] 清潔舊檔案...
if exist bin rmdir /s /q bin 2>nul
if exist build rmdir /s /q build 2>nul
if exist dist rmdir /s /q dist 2>nul

REM 編譯 APK
echo.
echo [4] 開始編譯 APK...
echo 請耐心等待（可能需要 10-30 分鐘）...

buildozer android debug

if %errorlevel% equ 0 (
    echo.
    echo ✓ APK 編譯成功
    
    REM 查找 APK 文件
    for /r "bin" %%f in (*.apk) do (
        set "APK_FILE=%%f"
        echo APK 位置: !APK_FILE!
    )
    
    REM 檢查是否有設備
    echo.
    echo [5] 檢查 Android 設備...
    adb devices
    
    echo.
    set /p install_choice="是否要安裝到設備？(Y/N): "
    
    if /i "%install_choice%"=="Y" (
        echo 正在安裝...
        adb install -r "!APK_FILE!"
        
        if %errorlevel% equ 0 (
            echo.
            echo ✓ APP 安裝成功
            echo 可以在設備上找到 "Jeff命理世界" 應用
        ) else (
            echo ✗ APP 安裝失敗
        )
    )
) else (
    echo.
    echo ✗ APK 編譯失敗
    echo 請檢查上面的錯誤訊息
    pause
    exit /b 1
)

echo.
echo 編譯過程完成！
pause
