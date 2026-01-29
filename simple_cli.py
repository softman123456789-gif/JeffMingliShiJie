#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jeff命理世界 - 命理分析系統
簡化版（用於打包成執行檔）
"""

import sys
from pathlib import Path
from datetime import datetime

# 設定路徑
BASE_PATH = Path(__file__).parent
MODULES_PATH = BASE_PATH / 'GITHUB' / 'modules'
GITHUB_PATH = BASE_PATH / 'GITHUB'

# 添加路徑
if MODULES_PATH.exists():
    sys.path.insert(0, str(MODULES_PATH))
if GITHUB_PATH.exists():
    sys.path.insert(0, str(GITHUB_PATH))

# 匯入命理模組
try:
    from mingli_jiugong import JiuGongAnalyzer
    from mingli_astrology import ZodiacSignAnalyzer
    from mingli_bazi_analyzer import BaziAnalyzer
    from mingli_purplestar_analyzer import PurpleStarAnalyzer
    from mingli_tarot import TarotAnalyzer
    from mingli_yijing import YijingAnalyzer
    print("[OK] 命理模組載入成功\n")
except Exception as e:
    print(f"[ERROR] 模組載入失敗: {e}\n")
    sys.exit(1)


def print_menu():
    """顯示主菜單"""
    print("=" * 60)
    print("  Jeff命理世界 v6.7 - 命理分析系統")
    print("=" * 60)
    print("\n選擇分析功能：")
    print("  1. 九宮分析（姓名數字分析）")
    print("  2. 星座分析（出生日期星座）")
    print("  3. 八字分析（出生年月日時）")
    print("  4. 紫微分析（紫微斗數）")
    print("  5. 塔羅牌（隨機卜卦）")
    print("  6. 周易卜卦（六爻分析）")
    print("  0. 離開程式")
    print("\n" + "=" * 60)


def analyze_jiugong():
    """九宮分析"""
    try:
        analyzer = JiuGongAnalyzer()
        name = input("請輸入姓名: ").strip()
        year = int(input("請輸入出生年份 (預設 1990): ") or "1990")
        month = int(input("請輸入出生月份 (預設 1): ") or "1")
        day = int(input("請輸入出生日期 (預設 1): ") or "1")
        
        result = analyzer.analyze_jiugong(name, year, month, day)
        print("\n" + "=" * 60)
        print(f"九宮分析結果 - {name}")
        print("=" * 60)
        print(result)
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n❌ 分析錯誤: {e}\n")


def analyze_astrology():
    """星座分析"""
    try:
        analyzer = ZodiacSignAnalyzer()
        month = int(input("請輸入出生月份 (1-12): "))
        day = int(input("請輸入出生日期 (1-31): "))
        
        result = analyzer.analyze_zodiac(month, day)
        print("\n" + "=" * 60)
        print("星座分析結果")
        print("=" * 60)
        print(result)
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n❌ 分析錯誤: {e}\n")


def analyze_bazi():
    """八字分析"""
    try:
        analyzer = BaziAnalyzer()
        year = int(input("請輸入出生年份: "))
        month = int(input("請輸入出生月份 (1-12): "))
        day = int(input("請輸入出生日期 (1-31): "))
        hour = int(input("請輸入出生時辰 (0-23, 預設 12): ") or "12")
        
        result = analyzer.analyze_bazi(year, month, day, hour)
        print("\n" + "=" * 60)
        print(f"八字分析結果 - {year}年{month}月{day}日 {hour}時")
        print("=" * 60)
        if isinstance(result, dict):
            for key, value in result.items():
                print(f"{key}: {value}")
        else:
            print(result)
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n❌ 分析錯誤: {e}\n")


def analyze_purplestar():
    """紫微分析"""
    try:
        analyzer = PurpleStarAnalyzer()
        year = int(input("請輸入出生年份: "))
        month = int(input("請輸入出生月份 (1-12): "))
        day = int(input("請輸入出生日期 (1-31): "))
        hour = int(input("請輸入出生時辰 (0-23): "))
        gender = input("請輸入性別 (M/F): ").upper()
        
        result = analyzer.analyze(year, month, day, hour, gender)
        print("\n" + "=" * 60)
        print("紫微分析結果")
        print("=" * 60)
        print(result)
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n❌ 分析錯誤: {e}\n")


def analyze_tarot():
    """塔羅牌"""
    try:
        analyzer = TarotAnalyzer()
        question = input("請輸入您的問題: ").strip()
        
        result = analyzer.draw_cards(num_cards=3)
        print("\n" + "=" * 60)
        print("塔羅牌卜卦結果")
        print("=" * 60)
        print(f"問題: {question}\n")
        print(result)
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n❌ 分析錯誤: {e}\n")


def analyze_yijing():
    """周易卜卦"""
    try:
        analyzer = YijingAnalyzer()
        question = input("請輸入您的問題: ").strip()
        
        result = analyzer.divinate()
        print("\n" + "=" * 60)
        print("周易卜卦結果")
        print("=" * 60)
        print(f"問題: {question}\n")
        print(result)
        print("=" * 60 + "\n")
    except Exception as e:
        print(f"\n❌ 分析錯誤: {e}\n")


def main():
    """主程式"""
    while True:
        print_menu()
        choice = input("請選擇 (0-6): ").strip()
        
        if choice == "0":
            print("\n謝謝使用 Jeff命理世界！")
            break
        elif choice == "1":
            analyze_jiugong()
        elif choice == "2":
            analyze_astrology()
        elif choice == "3":
            analyze_bazi()
        elif choice == "4":
            analyze_purplestar()
        elif choice == "5":
            analyze_tarot()
        elif choice == "6":
            analyze_yijing()
        else:
            print("\n❌ 無效選擇，請重新輸入！\n")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\n\n程式已中斷。謝謝使用！")
        sys.exit(0)
    except Exception as e:
        print(f"\n❌ 錯誤: {e}")
        sys.exit(1)
