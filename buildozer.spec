[app]

# 應用標題
title = Jeff命理世界

# 套件名稱（com.xxxx.yyyy 格式）
package.name = jiuyin_destiny

# 套件域名
package.domain = org.jiuyin

# 原始檔位置
source.dir = .

# 原始檔後綴名（Python 檔案）
source.include_exts = py,png,jpg,kv,atlas

# 要排除的目錄
source.exclude_dirs = tests, bin

# 版本號
version = 6.7

# 需求（Python 依賴）
requirements = python3,kivy,pillow,pyjnius

# 方向（portrait=直式, landscape=橫式, sensor=自動）
orientation = portrait

# 螢幕尺寸
fullscreen = 1

# Android API 等級
android.api = 31

# Android 最小 API 等級
android.minapi = 21

# Android NDK 版本
android.ndk = 25b

# 許可權設定
android.permissions = INTERNET,ACCESS_FINE_LOCATION,ACCESS_COARSE_LOCATION,WRITE_EXTERNAL_STORAGE,READ_EXTERNAL_STORAGE

# 功能設定
android.features = android.hardware.touchscreen

# 應用圖標
#icon.filename = %(source.dir)s/data/icon.png

# 應用啟動影像
#presplash.filename = %(source.dir)s/data/presplash.png

# 活動標籤
android.activity_label = @string/app_name

# 應用目標 API 等級
android.target_api = 31

# 使用 legacy 提高相容性
android.gradle_dependencies = 

# 允許備份
android.allow_backup = True

# 架構支援（armeabi-v7a, arm64-v8a, x86, x86_64）
android.archs = arm64-v8a

# 語言設定
android.locales = zh_TW

# Log 級別
log_level = 2
android.build_tools_version
=
31.0.0
