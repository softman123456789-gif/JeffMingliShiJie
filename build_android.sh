#!/bin/bash
# Android App 編譯和部署腳本（Linux/macOS）

echo "======================================"
echo "Jeff命理世界 - Android APP 編譯腳本"
echo "======================================"

# 設定顏色
GREEN='\033[0;32m'
RED='\033[0;31m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# 檢查環境
echo -e "\n${YELLOW}[1] 檢查環境變數...${NC}"

if [ -z "$ANDROID_SDK_ROOT" ]; then
    echo -e "${RED}✗ ANDROID_SDK_ROOT 未設定${NC}"
    echo "設定命令: export ANDROID_SDK_ROOT=\$HOME/Android/Sdk"
    exit 1
else
    echo -e "${GREEN}✓ ANDROID_SDK_ROOT: $ANDROID_SDK_ROOT${NC}"
fi

if [ -z "$JAVA_HOME" ]; then
    echo -e "${RED}✗ JAVA_HOME 未設定${NC}"
    exit 1
else
    echo -e "${GREEN}✓ JAVA_HOME: $JAVA_HOME${NC}"
fi

# 檢查必要工具
echo -e "\n${YELLOW}[2] 檢查必要工具...${NC}"

check_command() {
    if command -v $1 &> /dev/null; then
        echo -e "${GREEN}✓ $1${NC}"
    else
        echo -e "${RED}✗ $1 未安裝${NC}"
        return 1
    fi
}

check_command "python3"
check_command "java"
check_command "gradle"
check_command "buildozer"

# 建立 APK
echo -e "\n${YELLOW}[3] 開始編譯 APK...${NC}"

# 清潔舊檔案
rm -rf bin/ build/ dist/ .buildozer/

# 使用 buildozer 編譯
buildozer android debug

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✓ APK 編譯成功${NC}"
    APK_FILE=$(find bin -name "*.apk" -type f -printf '%T@ %p\n' | sort -rn | head -1 | cut -d' ' -f2-)
    echo -e "APK 位置: ${GREEN}$APK_FILE${NC}"
    
    # 安裝到設備
    echo -e "\n${YELLOW}[4] 安裝到 Android 設備...${NC}"
    adb install -r "$APK_FILE"
    
    if [ $? -eq 0 ]; then
        echo -e "${GREEN}✓ APP 安裝成功${NC}"
        echo -e "\n${GREEN}編譯和安裝完成！${NC}"
    else
        echo -e "${RED}✗ APP 安裝失敗${NC}"
    fi
else
    echo -e "${RED}✗ APK 編譯失敗${NC}"
    exit 1
fi
