# GitHub Actions Android 編譯設置指南

## 📋 概述

此設置使用 GitHub Actions 在雲端自動編譯 Android APK，無需本地複雜配置。

## 🚀 快速開始

### 步驟 1: 建立 GitHub 倉庫

1. 登入 GitHub (https://github.com)
2. 點擊 `+` → `New repository`
3. 填寫信息:
   - Repository name: `JeffMingliShiJie`
   - Description: `Jeff命理世界 - Kivy Android 應用`
   - 設為 Public (需要 free tier 中 Actions 免費額度)
   - 初始化: Add a README file

### 步驟 2: 複製文件到倉庫

```bash
# 克隆倉庫
git clone https://github.com/YOUR_USERNAME/JeffMingliShiJie.git
cd JeffMingliShiJie

# 複製所有應用文件
cp -r "G:\Coding Space\20250129_080713_v6.7.1\*" .

# 複製工作流文件
mkdir -p .github/workflows
cp "G:\Coding Space\20250129_080713_v6.7.1\.github\workflows\android-build.yml" .github/workflows/

# 推送到 GitHub
git add .
git commit -m "Initial commit - Jeff命理世界 v6.7.1"
git push origin main
```

### 步驟 3: 觸發編譯

**方式 A: 推送標籤 (推薦)**
```bash
# 建立版本標籤
git tag v6.7.1
git push origin v6.7.1
```

**方式 B: 推送到 main 分支 (自動編譯)**
```bash
git push origin main
```

### 步驟 4: 監控編譯進度

1. 進入 GitHub 倉庫頁面
2. 點擊 `Actions` 標籤
3. 查看正在進行的工作流
4. 等待完成 (通常 10-15 分鐘)

## 📊 工作流詳情

### 工作流文件位置
```
.github/workflows/android-build.yml
```

### 工作流步驟

1. **Checkout code** - 下載源代碼
2. **Setup Java** - 安裝 Java 11 (Android 開發所需)
3. **Setup Python** - 安裝 Python 3.10
4. **Install system dependencies** - 安裝必要的系統工具
5. **Install Python dependencies** - 安裝 buildozer 等 Python 包
6. **Setup Android SDK** - 安裝 Android SDK 和 NDK
7. **Build APK** - 執行 buildozer 編譯
8. **Upload artifacts** - 上傳 APK 至 GitHub Artifacts
9. **Create Release** - 建立 GitHub Release (帶 APK 下載)

## 📥 下載已編譯的 APK

### 下載方式 1: 從 Artifacts
1. 進入 GitHub 倉庫 → Actions
2. 選擇最新的編譯記錄
3. 向下捲動找到 "Artifacts"
4. 下載 `jeff-mingli-debug`

### 下載方式 2: 從 Release 頁面 (標籤編譯時)
1. 進入 GitHub 倉庫 → Releases
2. 找到對應版本 (e.g., v6.7.1)
3. 下載 APK 檔案

## 🔧 自訂工作流

### 修改編譯選項

編輯 `.github/workflows/android-build.yml`:

```yaml
- name: Build APK
  run: |
    buildozer android debug      # 改為 buildozer android release (生產版)
```

### 修改 Android 配置

編輯 `buildozer.spec`:

```ini
# 修改應用版本
version = 6.7.1

# 修改最小 API
android.minapi = 21

# 修改目標 API
android.target_api = 31
```

提交修改後會自動觸發新的編譯。

## ✅ 檢查清單

在設置前確認:

- [ ] GitHub 帳號已建立
- [ ] 本地安裝了 Git
- [ ] `buildozer.spec` 配置正確
- [ ] `main_android.py` 代碼無誤
- [ ] 所有必要文件已準備

## 📝 典型工作流

```
修改代碼
    ↓
git commit -am "Update features"
    ↓
git push origin main
    ↓
GitHub Actions 自動編譯 (10-15 分鐘)
    ↓
✅ APK 已準備好下載
```

或使用版本標籤:

```
完成新版本
    ↓
git tag v6.7.2
    ↓
git push origin v6.7.2
    ↓
GitHub Actions 自動編譯並建立 Release
    ↓
✅ APK 在 Release 頁面可下載
```

## 🐛 故障排除

### 編譯失敗 - 檢查項目

1. **Python 版本**: 必須是 3.10
   - 編輯 `.github/workflows/android-build.yml`
   - 找到 `python-version: '3.10'`

2. **buildozer.spec**: 檢查是否有重複或錯誤的配置
   - 執行 `buildozer --version`
   - 檢查配置語法

3. **Android API 版本**: 確認 SDK 版本相匹配
   - `api-level: 31` 必須與 `android.target_api = 31` 一致

4. **查看編譯日誌**:
   - Actions 頁面 → 選擇失敗的工作流
   - 展開各個步驟查看錯誤信息

### 常見錯誤

**錯誤 1: "Permission denied"**
- 原因: 未授予 GitHub Actions 權限
- 解決: 倉庫 Settings → Actions → Permissions → 允許所有操作

**錯誤 2: "Out of memory"**
- 原因: 編譯需要大量記憶體
- 解決: 在 buildozer.spec 中減少並行任務

**錯誤 3: "NDK not found"**
- 原因: Android NDK 版本不匹配
- 解決: 編輯工作流中的 `ndk-version`

## 💡 高級用法

### 自動發佈到 Google Play Store

可添加額外步驟上傳 APK 到 Google Play Store:

```yaml
- name: Upload to Play Store
  uses: r0adkll/upload-google-play@v1
  with:
    serviceAccountJsonPlainText: ${{ secrets.PLAY_STORE_KEY }}
    packageName: com.jiuyin_destiny.jingmingli
    releaseFiles: 'bin/*.apk'
    track: internal
```

### 自動建立 GitHub Release

已配置在工作流中 (參見 `Create Release` 步驟)

### 定期編譯

每天自動編譯一次:

```yaml
on:
  schedule:
    - cron: '0 0 * * 0'  # 每週日午夜
  push:
    tags:
      - 'v*'
```

## 📞 支援

如遇任何問題:

1. 查看 GitHub Actions 日誌 (Actions → 選擇工作流)
2. 檢查 `buildozer.spec` 配置
3. 參考 Buildozer 官方文檔 (https://buildozer.readthedocs.io)

## 🎉 完成

設置完成後，每次推送代碼時都會自動編譯 APK！

---

**工作流文件**: `.github/workflows/android-build.yml`
**編譯時間**: ~10-15 分鐘
**費用**: 免費 (GitHub Actions 免費額度)
**支援平台**: Ubuntu Latest
