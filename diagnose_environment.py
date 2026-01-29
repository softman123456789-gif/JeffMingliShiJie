#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
環境檢查和診斷腳本
用於驗證 Android 開發環境是否正確配置
"""

import os
import sys
import subprocess
from pathlib import Path

def print_section(title):
    """打印分隔符"""
    print(f"\n{'='*60}")
    print(f"  {title}")
    print(f"{'='*60}\n")

def check_command(cmd, name=None):
    """檢查命令是否可用"""
    name = name or cmd
    try:
        result = subprocess.run([cmd, '--version'], 
                              capture_output=True, 
                              text=True,
                              timeout=5)
        version = result.stdout.split('\n')[0]
        print(f"  ✓ {name:20} {version[:50]}")
        return True
    except:
        print(f"  ✗ {name:20} [未安裝或未在 PATH 中]")
        return False

def check_env_var(var_name):
    """檢查環境變數"""
    value = os.environ.get(var_name)
    if value:
        print(f"  ✓ {var_name:25} {value[:50]}")
        return True
    else:
        print(f"  ✗ {var_name:25} [未設定]")
        return False

def check_python_module(module_name):
    """檢查 Python 模組"""
    try:
        __import__(module_name)
        print(f"  ✓ {module_name:20} [已安裝]")
        return True
    except ImportError:
        print(f"  ✗ {module_name:20} [未安裝]")
        return False

def main():
    print_section("Jeff命理世界 - Android 環境診斷")
    
    # 1. 系統信息
    print_section("1. 系統信息")
    print(f"  操作系統: {sys.platform}")
    print(f"  Python 版本: {sys.version.split()[0]}")
    print(f"  工作目錄: {os.getcwd()}")
    
    # 2. 檢查必要命令
    print_section("2. 核心工具檢查")
    
    required_tools = {
        'java': 'Java OpenJDK',
        'python': 'Python',
        'git': 'Git',
    }
    
    tools_ok = True
    for cmd, name in required_tools.items():
        if not check_command(cmd, name):
            tools_ok = False
    
    # 3. 檢查環境變數
    print_section("3. 環境變數檢查")
    
    env_vars = [
        'ANDROID_SDK_ROOT',
        'JAVA_HOME',
        'ANDROID_HOME',
    ]
    
    for var in env_vars:
        check_env_var(var)
    
    # 4. 檢查 Android 工具
    print_section("4. Android 工具檢查")
    
    android_tools = {
        'adb': 'Android Debug Bridge',
        'emulator': 'Android Emulator',
        'gradle': 'Gradle Build System',
    }
    
    for cmd, name in android_tools.items():
        check_command(cmd, name)
    
    # 5. 檢查 Python 模組
    print_section("5. Python 模組檢查")
    
    python_modules = [
        'kivy',
        'pillow',
        'buildozer',
        'cython',
        'pyjnius',
    ]
    
    modules_ok = True
    for module in python_modules:
        if not check_python_module(module):
            modules_ok = False
    
    # 6. 檢查命理模組
    print_section("6. 命理模組檢查")
    
    github_path = Path(__file__).parent / 'GITHUB' / 'modules'
    if github_path.exists():
        modules_path = list(github_path.glob('*.py'))
        print(f"  找到 {len(modules_path)} 個命理模組:")
        for module_file in sorted(modules_path)[:5]:
            print(f"    - {module_file.name}")
        if len(modules_path) > 5:
            print(f"    ... 等 {len(modules_path)-5} 個模組")
    else:
        print(f"  ✗ 命理模組路徑不存在: {github_path}")
    
    # 7. 檢查編譯腳本
    print_section("7. 編譯工具檢查")
    
    base_path = Path(__file__).parent
    scripts = [
        'main_android.py',
        'buildozer.spec',
        'build_android.bat',
        'build_android.sh',
    ]
    
    for script in scripts:
        script_path = base_path / script
        if script_path.exists():
            print(f"  ✓ {script}")
        else:
            print(f"  ✗ {script} [缺失]")
    
    # 8. 建議
    print_section("8. 配置建議")
    
    if not tools_ok or not modules_ok:
        print("  ⚠️  存在缺失的工具或模組，請執行以下命令:")
        print()
        print("  Windows PowerShell:")
        print("    # 安裝 Python 依賴")
        print("    pip install kivy pillow buildozer cython pyjnius")
        print()
        print("    # 設定環境變數")
        print("    $env:ANDROID_SDK_ROOT = 'C:\\Users\\jeff6\\AppData\\Local\\Android\\Sdk'")
        print("    $env:JAVA_HOME = 'C:\\Program Files\\OpenJDK\\jdk-25'")
        print()
        print("  Linux/macOS:")
        print("    # 安裝 Python 依賴")
        print("    pip3 install kivy pillow buildozer cython pyjnius")
        print()
        print("    # 設定環境變數")
        print("    export ANDROID_SDK_ROOT=$HOME/Android/Sdk")
        print("    export JAVA_HOME=/usr/lib/jvm/java-17-openjdk")
    else:
        print("  ✅ 所有必要環境都已配置完成！")
        print()
        print("  可以立即開始編譯 Android App:")
        print()
        print("  本地測試:")
        print("    python main_android.py")
        print()
        print("  編譯 APK:")
        print("    .\\build_android.bat              # Windows")
        print("    bash ./build_android.sh           # Linux/macOS")
        print()
        print("  或使用 buildozer:")
        print("    buildozer android debug")
    
    print_section("診斷完成")
    
    return 0 if (tools_ok and modules_ok) else 1


if __name__ == '__main__':
    sys.exit(main())
