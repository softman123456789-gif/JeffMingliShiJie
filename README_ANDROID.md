# Android App 編譯與部署指南

## 項目概述
此專案將 Windows 桌面版 **Jeff命理世界 v6.7** 轉換為 **Android 移動應用**。

## 專案結構
```
andorid_app/
├── GITHUB/                    # 原始 Windows 程式碼
│   ├── modules/              # 命理分析模組
│   ├── mingli_suite_v6.7_ultimate_expert.py  # 原 Windows 主程式
│   └── README.md
├── main_android.py           # Android 版主程式（Kivy）
├── main.kv                   # Kivy UI 配置文件
├── buildozer.spec            # Buildozer 編譯配置
├── android/                  # Android 原生配置
│   ├── build.gradle          # Gradle 構建配置
│   ├── app/src/main/
│   │   ├── AndroidManifest/  # Android 應用清單
│   │   └── res/              # 資源文件
│   └── build.gradle
└── README_ANDROID.md         # 本檔案
```

## 所需環境

### 已安裝
- ✅ Java Development Kit 17 (OpenJDK)
- ✅ Android Studio 2025.2.3.9
- ✅ Git 2.52.0
- ✅ Python 3.14.2
- ✅ Kivy 框架

### 額外需要（如使用 Buildozer 編譯）

#### Windows 上編譯需要:
1. **Buildozer** - Python 2 Android 編譯工具
2. **Cython** - Python 轉 C 編譯器
3. **Java Development Kit** (已安裝)
4. **Android SDK** (已由 Android Studio 提供)
5. **Apache Ant** - 構建工具
6. **Git** (已安裝)

```bash
pip install buildozer cython
```

## 編譯方法

### 方法 1：使用 Android Studio（推薦）

1. **開啟 Android Studio**
   ```
   android-studio.exe
   ```

2. **開啟 Android 專案**
   - File → Open → 選擇 `G:\Coding Space\andorid_app\android` 資料夾
   - 等待 Gradle 同步完成

3. **配置 SDK**
   - Tools → SDK Manager
   - 安裝:
     - Android 13 (API 33)
     - Android 12 (API 31) - 推薦
     - Android 11 (API 30)
   - 建議勾選 Google Play Services

4. **建立 AVD 模擬器**
   - Tools → Device Manager
   - 點擊 "Create device"
   - 選擇 "Pixel 4" 或 "Pixel 5" 設備
   - 選擇 Android 12 系統映像
   - 完成建立

5. **編譯與執行**
   - 連接 Android 設備或啟動模擬器
   - Run → Run 'app'
   - 或按 `Shift + F10`

### 方法 2：使用 Buildozer（命令列）

#### 前置準備（如未安裝）

1. **安裝 Buildozer**
   ```powershell
   pip install buildozer
   ```

2. **安裝依賴工具**
   - 下載 Apache Ant：https://ant.apache.org/bindownload.cgi
   - 解壓並添加到 PATH
   - 驗證：`ant -version`

3. **設定環境變數**
   ```powershell
   # 設定 ANDROID_SDK_ROOT
   $env:ANDROID_SDK_ROOT = "C:\Users\[YourUsername]\AppData\Local\Android\Sdk"
   
   # 設定 JAVA_HOME
   $env:JAVA_HOME = "C:\Program Files\OpenJDK\jdk-17"
   ```

#### 編譯步驟

1. **導航到專案目錄**
   ```powershell
   cd "G:\Coding Space\andorid_app"
   ```

2. **初始化 Buildozer**
   ```powershell
   buildozer android debug
   ```

3. **監看編譯過程**
   ```powershell
   buildozer android debug -- --verbose
   ```

4. **輸出文件**
   - 編譯成功後會產生 `.apk` 檔案
   - 位置: `bin/jeff_mingliapp-0.1-debug.apk`

### 方法 3：使用 Gradle（命令列）

```powershell
# 進入 android 目錄
cd "G:\Coding Space\andorid_app\android"

# 清潔專案
gradlew clean

# 編譯 debug 版本
gradlew assembleDebug

# 編譯 release 版本（需要簽署金鑰）
gradlew assembleRelease
```

## 執行應用

### 在 Android 設備上執行

1. **使用 USB 連接**
   - 用 USB 線連接 Android 設備
   - 在設備上啟用 USB 調試模式
   - Android Studio 自動偵測

2. **使用 Android Studio 執行**
   ```
   Run → Run 'app'
   ```

3. **使用 ADB 手動安裝**
   ```powershell
   adb install -r bin\JeffMingliApp-0.1-debug.apk
   ```

### 在模擬器上執行

1. **啟動 AVD 模擬器**
   ```powershell
   # 列出可用設備
   emulator -list-avds
   
   # 啟動模擬器（例如：Pixel_4_API_31）
   emulator -avd Pixel_4_API_31
   ```

2. **使用 Android Studio 執行**
   - 模擬器啟動後，執行應用

## 功能說明

### 已實現的功能
- ✅ **九宮分析** - 姓名筆畫分析
- ✅ **星座分析** - 出生日期與血型分析
- ✅ **八字分析** - 年月日時八字推算

### 開發中的功能
- 🔨 **紫微分析** - 紫微斗數分析
- 🔨 **塔羅牌** - 塔羅牌卜卦
- 🔨 **周易卜卦** - 周易卦象分析
- 🔨 **血型分析** - 詳細血型性格分析
- 🔨 **名字分析** - 進階名字品質分析

## 常見問題

### Q: 編譯時出現 "No module named 'pyjnius'"
**A:** Pyjnius 是 Java/Python 互通庫，安裝：
```powershell
pip install pyjnius
```

### Q: Android SDK 未找到
**A:** 設定環境變數：
```powershell
$env:ANDROID_SDK_ROOT = "C:\Users\jeff6\AppData\Local\Android\Sdk"
```

### Q: Buildozer 提示找不到 Android NDK
**A:** NDK 會在首次編譯時自動下載。如需手動安裝：
1. 開啟 Android Studio
2. Tools → SDK Manager → SDK Tools
3. 勾選 "NDK (Side by side)"
4. 點擊 Apply 安裝

### Q: APK 檔案太大
**A:** 可採用以下優化措施：
- 移除未使用的模組
- 使用混淆 (Proguard)
- 分離 64 位/32 位架構

### Q: 應用在模擬器上執行緩慢
**A:**
- 確保模擬器有足夠 RAM (建議 4GB+)
- 啟用 KVM/HAXM 加速
- 使用 ARM64 架構而非 x86

## 發布到 Google Play Store

1. **建立簽署金鑰**
   ```powershell
   keytool -genkey -v -keystore my-release-key.keystore `
     -keyalg RSA -keysize 2048 -validity 10000 `
     -alias my-key-alias
   ```

2. **編譯 Release APK**
   ```powershell
   gradlew assembleRelease
   ```

3. **註冊 Google Play Developer 帳戶**
   - https://play.google.com/console

4. **上傳 APK**
   - Release management → App releases
   - 上傳簽署的 APK

## 開發提示

### 新增命理分析功能

1. 在 `main_android.py` 中新增 Screen 類別
2. 實現 `build_ui()` 方法設計 UI
3. 在 `MainScreen` 的功能按鈕中添加入口

### 除錯

```powershell
# 查看 Android logcat
adb logcat

# 監看特定應用日誌
adb logcat | findstr /i "JeffMingliApp"

# 列表設備
adb devices
```

## 技術棧

| 組件 | 版本 | 用途 |
|------|------|------|
| Kivy | 2.0+ | UI 框架 |
| Python | 3.14.2 | 運行環境 |
| Android SDK | 31+ | 開發工具 |
| Gradle | 7.0+ | 構建工具 |
| Java | OpenJDK 17 | JVM 語言 |

## 許可權說明

應用請求的 Android 許可權：
- `INTERNET` - 網路連接（預留功能）
- `READ_EXTERNAL_STORAGE` - 讀取文件
- `WRITE_EXTERNAL_STORAGE` - 寫入分析結果
- `ACCESS_FINE_LOCATION` - 精確定位（預留功能）
- `ACCESS_COARSE_LOCATION` - 粗略定位（預留功能）

## 性能最佳化

1. **使用 ProGuard 代碼混淆和優化**
   ```gradle
   minifyEnabled true
   proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
   ```

2. **分離 ABI 以減少 APK 大小**
   ```gradle
   splits {
       abi {
           enable true
           reset()
           include 'arm64-v8a', 'armeabi-v7a'
       }
   }
   ```

3. **使用 Android Profiler 分析**
   - Run → Profiler
   - 監看 CPU、記憶體使用情況

## 下一步

1. ✅ 基礎 UI 框架完成
2. ✅ 命理模組整合
3. 🔜 完成所有命理功能
4. 🔜 美化 UI 設計
5. 🔜 優化性能
6. 🔜 發布測試版本
7. 🔜 上傳到 Google Play Store

## 支援

如有問題，請檢查：
1. 所有必要工具已安裝
2. Android SDK 已同步更新
3. Python 依賴庫已安裝
4. 環境變數已正確設定

祝你開發順利！ 🎉
