#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
快速測試腳本 - 驗證 Kivy 應用在本地運行
可用於測試 UI 和命理模組整合
"""

import sys
import os
from pathlib import Path

# 設定路徑
BASE_PATH = Path(__file__).parent
MODULES_PATH = BASE_PATH / 'GITHUB' / 'modules'
GITHUB_PATH = BASE_PATH / 'GITHUB'

# 添加路徑
if MODULES_PATH.exists():
    sys.path.insert(0, str(MODULES_PATH))
if GITHUB_PATH.exists():
    sys.path.insert(0, str(GITHUB_PATH))

print("=" * 60)
print("Jeff命理世界 - 本地測試環境")
print("=" * 60)

# 檢查依賴
print("\n[1] 檢查必要依賴...")
missing_modules = []

required_modules = ['kivy', 'pillow']
for module in required_modules:
    try:
        __import__(module)
        print(f"  ✓ {module}")
    except ImportError:
        print(f"  ✗ {module}")
        missing_modules.append(module)

if missing_modules:
    print(f"\n缺少以下模組: {', '.join(missing_modules)}")
    print("請執行: pip install " + " ".join(missing_modules))
    sys.exit(1)

# 檢查命理模組
print("\n[2] 檢查命理模組...")
modules_to_check = [
    'mingli_astrology',
    'mingli_bazi_analyzer',
    'mingli_blood_type_enhanced',
    'mingli_purplestar_analyzer',
    'mingli_tarot',
    'mingli_yijing',
    'mingli_jiugong',
    'mingli_jiugong_name_enhanced',
]

for mod in modules_to_check:
    try:
        __import__(mod)
        print(f"  ✓ {mod}")
    except ImportError as e:
        print(f"  ✗ {mod} - {e}")

# 啟動 Kivy 應用
print("\n[3] 啟動 Kivy 應用...")
print("-" * 60)

try:
    from main_android import JeffMingliApp
    print("✓ 命理應用已載入，正在啟動...")
    app = JeffMingliApp()
    app.run()
except Exception as e:
    print(f"✗ 應用啟動失敗: {e}")
    import traceback
    traceback.print_exc()
    sys.exit(1)
