# 🚀 完整的 GitHub 上傳指南 - 一步一步

## 前置準備 ✅

- ✅ Git 已安裝 (2.52.0)
- ✅ GitHub 帳號已建立
- ✅ 所有代碼檔案已準備
- ✅ 工作流配置已就位 (.github/workflows/android-build.yml)

## 📋 完整步驟 (預計 15-20 分鐘)

### 第 1 步: 本地 Git 初始化 (5 分鐘)

#### 方法 A: 使用自動化腳本 (推薦)

**Windows 命令提示符 (CMD)**:
```batch
cd G:\Coding Space\20250129_080713_v6.7.1
setup_github.bat
```

**PowerShell**:
```powershell
cd "G:\Coding Space\20250129_080713_v6.7.1"
powershell -ExecutionPolicy Bypass -File setup_github.ps1
```

腳本將自動完成:
- ✅ 配置 Git 用戶名和郵箱
- ✅ 初始化本地 Git 倉庫
- ✅ 添加所有文件
- ✅ 建立初始提交
- ✅ 建立版本標籤 (v6.7.1)

#### 方法 B: 手動操作

```bash
cd G:\Coding Space\20250129_080713_v6.7.1

# 配置 Git
git config --global user.name "您的GitHub用戶名"
git config --global user.email "您的郵箱@example.com"

# 初始化倉庫
git init

# 添加所有文件
git add .

# 建立提交
git commit -m "Initial commit - Jeff命理世界 v6.7.1"

# 建立標籤
git tag v6.7.1
```

### 第 2 步: 在 GitHub 建立遠端倉庫 (5 分鐘)

1. **登入 GitHub**
   - 進入 https://github.com
   - 登入您的帳號

2. **建立新倉庫**
   - 點擊右上角的 `+` 按鈕
   - 選擇 `New repository`

3. **填寫倉庫信息**
   ```
   Repository name:     JeffMingliShiJie
   Description:         Jeff命理世界 - Kivy Android 應用
   Public/Private:      Public (免費 Actions 需要)
   Initialize:          ❌ 不要初始化任何檔案
   ```

4. **點擊 `Create repository`**

5. **複製倉庫 URL**
   - 看到 "Quick setup" 頁面
   - 複製 HTTPS URL (推薦)
   - 例如: `https://github.com/YOUR_USERNAME/JeffMingliShiJie.git`

### 第 3 步: 推送代碼到 GitHub (5 分鐘)

在您的本地目錄執行:

```bash
# 添加遠端倉庫 (使用您複製的URL)
git remote add origin https://github.com/YOUR_USERNAME/JeffMingliShiJie.git

# 將主分支改名為 main (GitHub 預設)
git branch -M main

# 推送主分支
git push -u origin main

# 推送標籤 (觸發 GitHub Actions 編譯)
git push origin v6.7.1
```

✅ 代碼已推送到 GitHub！

### 第 4 步: 監控 GitHub Actions 編譯 (自動 10-15 分鐘)

1. **進入 GitHub Actions**
   - 進入您的倉庫頁面
   - 點擊 `Actions` 標籤
   - 應該看到 "Build Android APK" 工作流正在執行

2. **查看編譯進度**
   - 綠色圖標 = 執行中 ⏳
   - 紅色圖標 = 失敗 ❌
   - 綠色打勾 = 成功 ✅

3. **查看詳細日誌**
   - 點擊工作流記錄
   - 展開各個步驟查看詳情

### 第 5 步: 下載編譯完成的 APK (編譯完成後)

#### 方式 1: 從 Artifacts (推薦快速下載)

```
Actions 頁面
  → 點擊最新的編譯記錄 "Build Android APK"
  → 向下捲動至 "Artifacts" 區域
  → 下載 "jeff-mingli-debug" 檔案 (.zip)
  → 解壓縮得到 .apk 檔案
```

#### 方式 2: 從 Release

```
倉庫主頁
  → 右側 "Releases" 區域
  → 點擊 "v6.7.1" Release
  → 在 "Assets" 中下載 .apk 檔案
```

## ✅ 驗證步驟

### 本地驗證

執行以下命令確認本地設置:

```bash
# 檢查 Git 配置
git config --list | findstr user

# 檢查提交歷史
git log --oneline

# 檢查標籤
git tag

# 檢查遠端倉庫
git remote -v
```

### GitHub 驗證

1. ✅ 倉庫頁面可見所有文件
2. ✅ `.github/workflows/android-build.yml` 在 Code 標籤可見
3. ✅ Actions 標籤顯示編譯記錄
4. ✅ Releases 顯示 v6.7.1 標籤

## 🐛 故障排除

### 推送失敗 - "Authentication failed"

**原因**: Git 認證失敗

**解決**:
1. 生成 Personal Access Token
   - GitHub 設定 → Developer settings → Personal access tokens
   - 建立新 token (勾選 `repo` 權限)
   
2. 使用 Token 推送
   ```bash
   git remote remove origin
   git remote add origin https://YOUR_TOKEN@github.com/YOUR_USERNAME/JeffMingliShiJie.git
   git push -u origin main
   git push origin v6.7.1
   ```

### 推送失敗 - "rejected"

**原因**: 遠端倉庫非空或已有不同的歷史

**解決**:
```bash
# 強制推送 (使用 Token 認證)
git push -u origin main --force
git push origin v6.7.1 --force
```

### Actions 編譯失敗

**檢查步驟**:
1. 點擊失敗的工作流
2. 查看各個步驟的詳細日誌
3. 檢查 `buildozer.spec` 配置
4. 查看 `ANDROID_COMPILE_REPORT.md` 中的故障排除

### APK 未出現在 Artifacts

**原因**: 編譯失敗或工作流未正確配置

**檢查**:
1. 工作流是否執行成功 (綠色打勾)
2. 檢查日誌中的「Build APK」步驟
3. 確認 `.github/workflows/android-build.yml` 檔案無誤

## 🎯 常見問題

### Q: 编译需要多久?
**A**: 首次编译 15-20 分鐘，後續編譯 10-15 分鐘

### Q: 可以修改代码后自動編譯嗎?
**A**: 可以！任何推送到 `main` 分支都會自動編譯

### Q: 如何建立新版本?
```bash
# 修改代碼
# ...

# 提交
git add .
git commit -m "New features"

# 建立新標籤
git tag v6.7.2
git push origin main
git push origin v6.7.2
```

### Q: APK 如何安裝到手機?
**A**: 
1. 下載 .apk 檔案到電腦
2. 連接 Android 手機 (開啟開發者選項)
3. 執行: `adb install 檔案名.apk`
4. 或將 .apk 複製到手機，點擊安裝

## 📊 完整工作流圖

```
修改代碼 (可選)
    ↓
建立提交和標籤 (本地)
    ↓
git push origin main
    ↓
GitHub Actions 自動觸發
    ↓
編譯環境設置 (2-5 分鐘)
    ↓
Buildozer 編譯 APK (5-12 分鐘)
    ↓
上傳至 Artifacts/Release (自動)
    ↓
✅ 完成！可下載 APK
```

## ⏱️ 時間規劃

| 步驟 | 耗時 |
|-----|------|
| 本地 Git 初始化 | 5 分鐘 |
| GitHub 倉庫建立 | 5 分鐘 |
| 代碼推送 | 5 分鐘 |
| 自動編譯 | 10-15 分鐘 |
| **總計** | **20-30 分鐘** |

## 🎉 完成檢查清單

- [ ] 本地 Git 已初始化
- [ ] 已在 GitHub 建立倉庫
- [ ] 代碼已推送到 main 分支
- [ ] 標籤已推送 (v6.7.1)
- [ ] GitHub Actions 工作流正在執行
- [ ] 編譯完成 ✅
- [ ] APK 已下載

## 📞 需要幫助?

查看這些文檔:
- `GITHUB_ACTIONS_QUICK_START.md` - 快速開始
- `GITHUB_ACTIONS_SETUP.md` - 詳細設置
- `ANDROID_COMPILE_REPORT.md` - 故障排除

---

**預計完成時間**: 20-30 分鐘
**難度**: ⭐ 簡單 (大部分自動化)
**結果**: 可用的 Android APK 檔案

祝您成功！🚀
