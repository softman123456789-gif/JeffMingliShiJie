# 🚀 Android App 編譯快速指南

## 📱 一句話開始

```powershell
# 本地測試（無需 Android 設備）
python main_android.py

# 編譯 Android APK
.\build_android.bat
```

---

## ✅ 當前狀態檢查

首先檢查環境是否已完全配置：

```powershell
python diagnose_environment.py
```

如果所有項目都標記為 ✓，表示已準備好編譯！

---

## 🛠️ 編譯方法（三選一）

### 方法 1️⃣：自動編譯腳本（推薦）

**最簡單的方式 - 全自動！**

```powershell
cd "G:\Coding Space\andorid_app"
.\build_android.bat
```

脚本會自動完成：
- ✅ 檢查環境變數
- ✅ 清潔舊檔案
- ✅ 編譯 APK
- ✅ 安裝到設備
- ✅ 啟動應用

---

### 方法 2️⃣：Buildozer 命令行

**適合喜歡手動控制的開發者**

```powershell
cd "G:\Coding Space\andorid_app"

# 設定環境變數（首次）
$env:ANDROID_SDK_ROOT = "C:\Users\jeff6\AppData\Local\Android\Sdk"
$env:JAVA_HOME = "C:\Program Files\OpenJDK\jdk-25"

# 編譯 debug APK（快速）
buildozer android debug

# 或編譯 release APK（用於發布）
buildozer android release
```

編譯成功後，APK 文件位置：
```
bin/jiuyin_destiny-6.7-debug.apk
```

---

### 方法 3️⃣：Android Studio 圖形界面

**最直觀的方式 - 適合新手**

1. **開啟 Android Studio**
   ```powershell
   android-studio.exe
   ```

2. **打開項目**
   - File → Open → 選擇 `G:\Coding Space\andorid_app\android`
   - 等待 Gradle 同步（5-10 分鐘）

3. **連接設備**
   - USB 線連接 Android 手機，或
   - Tools → Device Manager 啟動虛擬機

4. **執行應用**
   - Run → Run 'app'（或按 Shift+F10）

---

## 📲 在哪裡運行

### 選項 A：Android 真機（推薦）
```powershell
# 用 USB 連接手機
# 設置 → 關於手機 → 連續點擊版本號啟用開發者選項
# 設置 → 開發者選項 → USB 偵錯 ON

# 檢查連接
adb devices

# 安裝應用
adb install -r bin\jiuyin_destiny-6.7-debug.apk

# 手機上會出現 "Jeff命理世界" 應用圖標
```

### 選項 B：Android 模擬器
```powershell
# 啟動模擬器
emulator -avd Pixel_4_API_31

# 等待模擬器完全啟動（3-5 分鐘）

# 安裝應用
adb install -r bin\jiuyin_destiny-6.7-debug.apk

# 在模擬器上運行
```

### 選項 C：本地 PC 測試（開發時最快）
```powershell
# 無需 Android 設備，直接在 PC 運行
python main_android.py

# 會彈出 Kivy 應用窗口
# 適合快速測試 UI 和邏輯
```

---

## 🐛 常見問題快速解決

| 問題 | 解決方案 |
|------|--------|
| **找不到 buildozer** | `pip install buildozer` |
| **找不到 Android SDK** | 設定 `$env:ANDROID_SDK_ROOT` |
| **編譯很慢** | 首次下載 NDK，耐心等待 |
| **APK 太大（>100MB）** | 移除未使用模組 |
| **設備檢測不到** | `adb devices` 查看 |
| **模擬器太慢** | 啟用 KVM/HAXM 加速 |

---

## 📊 編譯進度預估

| 步驟 | 時間 |
|------|------|
| 環境檢查 | ~1 分鐘 |
| 下載依賴 | ~5-10 分鐘（首次） |
| 編譯代碼 | ~10-15 分鐘 |
| 生成 APK | ~5 分鐘 |
| **總計** | **20-30 分鐘（首次）** |

後續編譯會更快（5-10 分鐘）

---

## ✨ 編譯成功的標誌

當看到這些訊息時，表示編譯成功 ✅

```
✓ APK 編譯成功
APK 位置: bin/jiuyin_destiny-6.7-debug.apk

✓ APP 安裝成功

✓ 應用已啟動
```

手機/模擬器上會出現 **"Jeff命理世界"** 應用

---

## 📝 編譯配置說明

### buildozer.spec 主要參數

```ini
[app]
title = Jeff命理世界                    # 應用名稱
package.name = jiuyin_destiny           # 包名（英文）
package.domain = org.jiuyin             # 域名
version = 6.7                           # 版本號

[app:android]
android.api = 31                        # Android API 等級
android.minapi = 21                     # 最低 API 等級
android.archs = arm64-v8a               # CPU 架構（64位）

requirements = python3,kivy,pillow      # Python 依賴
```

---

## 🔍 調試技巧

### 查看實時日誌
```powershell
# 連接設備後查看應用日誌
adb logcat | findstr "jiuyin_destiny"

# 或查看所有日誌
adb logcat
```

### 檢查設備資訊
```powershell
adb devices -l              # 列表所有設備
adb shell getprop           # 查看設備屬性
adb shell pm list packages  # 列表已安裝應用
```

### 清除應用數據
```powershell
adb uninstall org.jiuyin.destiny  # 卸載應用
adb shell pm clear org.jiuyin.destiny  # 清除數據
```

---

## 📚 詳細文檔

更詳細的信息請參考：

- **完整指南**: [README_ANDROID.md](README_ANDROID.md)
- **轉換報告**: [CONVERSION_COMPLETE.md](CONVERSION_COMPLETE.md)
- **環境診斷**: `python diagnose_environment.py`

---

## 🎯 下一步

**立即開始：**

```powershell
# 1. 檢查環境
python diagnose_environment.py

# 2. 本地測試
python main_android.py

# 3. 編譯 APK
.\build_android.bat
```

祝編譯順利！🎉
