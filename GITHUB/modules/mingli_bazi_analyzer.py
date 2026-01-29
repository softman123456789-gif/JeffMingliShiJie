#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
八字排盤分析模組
提供完整的八字排盤、五行分析、命理解讀功能
修復 v2.2 版本的八字輸出問題
"""

from datetime import datetime, timedelta
from typing import Dict, List, Tuple
import random


class BaziAnalyzer:
    """八字排盤分析器"""

    # 天干 (10 個)
    HEAVENLY_STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    
    # 地支 (12 個)
    EARTHLY_BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 五行
    FIVE_ELEMENTS = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水',
        '寅': '木', '卯': '木',
        '巳': '火', '午': '火',
        '辰': '土', '戌': '土', '丑': '土', '未': '土',
        '申': '金', '酉': '金',
        '子': '水', '亥': '水'
    }
    
    # 地支五行衝突表
    CONFLICTS = {
        '子': '午', '午': '子',
        '丑': '未', '未': '丑',
        '寅': '申', '申': '寅',
        '卯': '酉', '酉': '卯',
        '辰': '戌', '戌': '辰',
        '巳': '亥', '亥': '巳'
    }

    # 十二地支對應時辰
    BRANCH_TO_HOUR = {
        '子': (23, 1), '丑': (1, 3), '寅': (3, 5), '卯': (5, 7),
        '辰': (7, 9), '巳': (9, 11), '午': (11, 13), '未': (13, 15),
        '申': (15, 17), '酉': (17, 19), '戌': (19, 21), '亥': (21, 23)
    }
    
    # 性格分析
    CHARACTER_ANALYSIS = {
        '甲': '領導型、進取心強、富有朝氣',
        '乙': '柔和型、藝術氣質、溫和有禮',
        '丙': '熱情型、性格開朗、善於表達',
        '丁': '文靜型、思維敏捷、做事細緻',
        '戊': '實幹型、穩重踏實、吃苦耐勞',
        '己': '謙虛型、包容力強、人際關係好',
        '庚': '剛毅型、做事果斷、耿直坦率',
        '辛': '靈活型、變通能力強、適應力強',
        '壬': '聰慧型、領悟力高、想像力豐富',
        '癸': '冷靜型、思考深入、內斂沉著',
    }
    
    # 五行性格
    ELEMENT_CHARACTER = {
        '木': '仁義、進取、創新',
        '火': '禮儀、聰慧、熱情',
        '土': '信用、穩重、厚道',
        '金': '義氣、堅強、果決',
        '水': '智慧、靈活、深沉'
    }

    def __init__(self):
        """初始化八字分析器"""
        self.lunar_to_solar_cache = {}

    def get_lunar_year_branch(self, year: int) -> str:
        """
        獲取農曆年份的地支
        鼠、牛、虎、兔、龍、蛇、馬、羊、猴、雞、狗、豬
        
        Args:
            year: 陽曆年份
            
        Returns:
            地支 (一個字)
        """
        # 1900 年是鼠年
        base_year = 1900
        offset = (year - base_year) % 12
        return self.EARTHLY_BRANCHES[offset]

    def get_lunar_month_branch(self, month: int, is_leap: bool = False) -> str:
        """
        獲取農曆月份的地支
        
        Args:
            month: 月份 (1-12)
            is_leap: 是否為閏月
            
        Returns:
            地支
        """
        # 農曆月份對應地支 (正月～十二月)
        months_branches = ['寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥', '子', '丑']
        return months_branches[(month - 1) % 12]

    def get_solar_stem_by_date(self, year: int, month: int, day: int) -> str:
        """
        根據陽曆日期計算天干
        (簡化算法，實際八字排盤需要根據節氣計算)
        
        Args:
            year: 年
            month: 月
            day: 日
            
        Returns:
            天干
        """
        # 簡化方法：根據日期計算
        total_days = 0
        for y in range(1900, year):
            total_days += 366 if self._is_leap_year(y) else 365
        
        for m in range(1, month):
            total_days += self._days_in_month(year, m)
        
        total_days += day
        
        return self.HEAVENLY_STEMS[total_days % 10]

    def get_hour_branch(self, hour: int) -> str:
        """
        根據小時計算地支
        
        Args:
            hour: 小時 (0-23)
            
        Returns:
            地支
        """
        if hour == 0:  # 午夜 23:00-01:00 是子時
            return '子'
        
        hour = hour % 24
        for branch, (start, end) in self.BRANCH_TO_HOUR.items():
            if start <= hour < end or (start > end and (hour >= start or hour < end)):
                return branch
        return '子'

    def get_hour_stem(self, day_stem: str, hour: int) -> str:
        """
        根據日幹和小時計算小時幹
        
        Args:
            day_stem: 日天干
            hour: 小時
            
        Returns:
            天干
        """
        # 根據日幹計算時幹（五子時論命法）
        day_stem_index = self.HEAVENLY_STEMS.index(day_stem)
        hour_branch = self.get_hour_branch(hour)
        hour_branch_index = self.EARTHLY_BRANCHES.index(hour_branch)
        
        # 時幹 = (日幹 + 時支) * 2
        hour_stem_index = (day_stem_index * 2 + hour_branch_index) % 10
        return self.HEAVENLY_STEMS[hour_stem_index]

    def analyze_bazi(self, year: int, month: int, day: int, hour: int = 12) -> Dict:
        """
        分析八字
        
        Args:
            year: 出生年
            month: 出生月
            day: 出生日
            hour: 出生時辰 (0-23)
            
        Returns:
            八字分析結果字典
        """
        try:
            # 1. 獲取基本八字
            year_stem = self.get_solar_stem_by_date(year, 1, 1)  # 年幹簡化版
            year_branch = self.get_lunar_year_branch(year)
            
            month_stem = self.get_solar_stem_by_date(year, month, 1)  # 月幹簡化版
            month_branch = self.get_lunar_month_branch(month)
            
            day_stem = self.get_solar_stem_by_date(year, month, day)
            day_branch = self.EARTHLY_BRANCHES[(day - 1) % 12]
            
            hour_stem = self.get_hour_stem(day_stem, hour)
            hour_branch = self.get_hour_branch(hour)
            
            # 2. 組合八字
            bazi = {
                'year': f"{year_stem}{year_branch}",
                'month': f"{month_stem}{month_branch}",
                'day': f"{day_stem}{day_branch}",
                'hour': f"{hour_stem}{hour_branch}"
            }
            
            # 3. 五行分析
            five_elements_count = {'木': 0, '火': 0, '土': 0, '金': 0, '水': 0}
            for stem_branch in bazi.values():
                for char in stem_branch:
                    if char in self.FIVE_ELEMENTS:
                        five_elements_count[self.FIVE_ELEMENTS[char]] += 1
            
            # 4. 納音五行 (簡化版)
            nayin_elements = self._calculate_nayin(year, month, day, hour)
            
            # 5. 十干十二支人格分析
            day_stem_character = self.CHARACTER_ANALYSIS.get(day_stem, '')
            
            # 6. 天干地支衝突檢查
            conflicts = self._check_conflicts(bazi)
            
            # 7. 組織結果
            result = {
                'success': True,
                'date': f"{year}年{month:02d}月{day:02d}日 {hour:02d}時",
                'bazi': bazi,
                'five_elements': five_elements_count,
                'nayin': nayin_elements,
                'day_stem_character': day_stem_character,
                'conflicts': conflicts,
                'analysis': self._generate_analysis(bazi, five_elements_count, conflicts),
                'suggestions': self._generate_suggestions(day_stem, five_elements_count)
            }
            
            return result
            
        except Exception as e:
            return {
                'success': False,
                'error': str(e),
                'message': '八字排盤失敗，請檢查輸入的日期是否正確'
            }

    def _is_leap_year(self, year: int) -> bool:
        """檢查是否為閏年"""
        return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)

    def _days_in_month(self, year: int, month: int) -> int:
        """獲取月份天數"""
        if month in [1, 3, 5, 7, 8, 10, 12]:
            return 31
        elif month in [4, 6, 9, 11]:
            return 30
        else:  # 2 月
            return 29 if self._is_leap_year(year) else 28

    def _calculate_nayin(self, year: int, month: int, day: int, hour: int) -> str:
        """計算納音五行 (簡化版)"""
        nayin_map = {
            0: '金', 1: '金', 2: '木', 3: '木', 4: '水', 
            5: '水', 6: '火', 7: '火', 8: '土', 9: '土'
        }
        
        # 簡化：年干的納音
        year_stem = self.get_solar_stem_by_date(year, 1, 1)
        year_stem_index = self.HEAVENLY_STEMS.index(year_stem)
        
        return nayin_map[year_stem_index % 10]

    def _check_conflicts(self, bazi: Dict) -> List[str]:
        """檢查八字中的衝突"""
        conflicts = []
        branches = [bazi['year'][1], bazi['month'][1], bazi['day'][1], bazi['hour'][1]]
        
        for i in range(len(branches)):
            for j in range(i + 1, len(branches)):
                if branches[i] in self.CONFLICTS:
                    if self.CONFLICTS[branches[i]] == branches[j]:
                        conflicts.append(f"{branches[i]}衝{branches[j]}")
        
        return conflicts

    def _generate_analysis(self, bazi: Dict, five_elements: Dict, conflicts: List) -> str:
        """生成八字分析文本"""
        analysis = "【八字排盤分析】\n"
        analysis += "="*50 + "\n\n"
        
        analysis += "【八字組合】\n"
        analysis += f"年: {bazi['year']}  月: {bazi['month']}\n"
        analysis += f"日: {bazi['day']}  時: {bazi['hour']}\n\n"
        
        analysis += "【五行統計】\n"
        total = sum(five_elements.values())
        for element, count in sorted(five_elements.items(), key=lambda x: x[1], reverse=True):
            percentage = (count / total * 100) if total > 0 else 0
            analysis += f"{element}: {count} 個 ({percentage:.1f}%)\n"
        
        analysis += "\n【命理說明】\n"
        
        # 五行平衡分析
        element_counts = list(five_elements.values())
        if max(element_counts) - min(element_counts) > 2:
            analysis += "五行不平衡，命格較為偏強或偏弱。\n"
        else:
            analysis += "五行相對均衡，命格較為穩定。\n"
        
        # 衝突分析
        if conflicts:
            analysis += f"\n【天支衝突】\n"
            for conflict in conflicts:
                analysis += f"⚠️ {conflict} - 易產生變化或挑戰\n"
        else:
            analysis += "\n天支無衝突，命格較為和諧。\n"
        
        return analysis

    def _generate_suggestions(self, day_stem: str, five_elements: Dict) -> str:
        """生成建議"""
        suggestions = "【改運建議】\n"
        
        # 性格建議
        character = self.CHARACTER_ANALYSIS.get(day_stem, '')
        if character:
            suggestions += f"性格特點: {character}\n"
        
        # 五行平衡建議
        max_element = max(five_elements.items(), key=lambda x: x[1])[0]
        min_element = min(five_elements.items(), key=lambda x: x[1])[0]
        
        suggestions += f"\n建議：\n"
        suggestions += f"1. 加強 {min_element} 五行的補充\n"
        suggestions += f"2. 從事與 {min_element} 相關的職業\n"
        suggestions += f"3. 配戴 {min_element} 屬性的飾品\n"
        
        return suggestions

    def format_result(self, result: Dict) -> str:
        """格式化結果為字符串"""
        if not result.get('success', False):
            return f"❌ 排盤失敗: {result.get('error', '未知錯誤')}"
        
        output = ""
        output += f"📅 出生時間: {result['date']}\n\n"
        output += result['analysis']
        output += "\n" + result['suggestions']
        
        return output


# 簡化的八字排盤快速版本
class SimpleBaziCalculator:
    """簡化版八字計算器 - 用於快速查詢"""
    
    STEMS = ['甲', '乙', '丙', '丁', '戊', '己', '庚', '辛', '壬', '癸']
    BRANCHES = ['子', '丑', '寅', '卯', '辰', '巳', '午', '未', '申', '酉', '戌', '亥']
    
    # 簡化的五行對應
    ELEMENT_MAP = {
        '甲': '木', '乙': '木',
        '丙': '火', '丁': '火',
        '戊': '土', '己': '土',
        '庚': '金', '辛': '金',
        '壬': '水', '癸': '水'
    }
    
    # 十二生肖
    ZODIACS = ['鼠', '牛', '虎', '兔', '龍', '蛇', '馬', '羊', '猴', '雞', '狗', '豬']
    
    @staticmethod
    def calculate_quick(year: int, month: int, day: int, hour: int = 12) -> str:
        """快速計算八字"""
        calc = SimpleBaziCalculator()
        
        # 計算年幹支
        year_offset = year - 1900
        year_stem = calc.STEMS[year_offset % 10]
        year_branch = calc.BRANCHES[year_offset % 12]
        zodiac = calc.ZODIACS[year_offset % 12]
        
        # 計算月幹支 (簡化版)
        month_branch = calc.BRANCHES[(month - 1) % 12]
        month_stem = calc.STEMS[(year_offset * 2 + month - 1) % 10]
        
        # 計算日幹支
        day_offset = (year - 1900) * 365 + sum(31 if m in [1,3,5,7,8,10,12] else 30 if m in [4,6,9,11] else 29 if (year % 4 == 0 and year % 100 != 0) or year % 400 == 0 else 28 for m in range(1, month)) + day
        day_stem = calc.STEMS[day_offset % 10]
        day_branch = calc.BRANCHES[day_offset % 12]
        
        # 計算時幹支
        hour_branch = calc.BRANCHES[hour // 2]
        hour_stem = calc.STEMS[(day_offset * 2 + hour // 2) % 10]
        
        # 計算五行
        elements = {}
        for stem in [year_stem, month_stem, day_stem, hour_stem]:
            elem = calc.ELEMENT_MAP.get(stem, '未知')
            elements[elem] = elements.get(elem, 0) + 1
        
        for branch in [year_branch, month_branch, day_branch, hour_branch]:
            # 地支五行對應
            branch_elem = {
                '子': '水', '丑': '土', '寅': '木', '卯': '木', '辰': '土', '巳': '火',
                '午': '火', '未': '土', '申': '金', '酉': '金', '戌': '土', '亥': '水'
            }.get(branch, '未知')
            elements[branch_elem] = elements.get(branch_elem, 0) + 1
        
        # 格式化輸出
        output = f"【八字快速查詢】\n"
        output += f"{"="*40}\n"
        output += f"出生年月日時: {year}年{month}月{day}日 {hour}時\n"
        output += f"生肖: {zodiac}\n\n"
        output += f"八字組合:\n"
        output += f"  年: {year_stem}{year_branch}\n"
        output += f"  月: {month_stem}{month_branch}\n"
        output += f"  日: {day_stem}{day_branch}\n"
        output += f"  時: {hour_stem}{hour_branch}\n\n"
        output += f"五行分布:\n"
        for elem, count in sorted(elements.items(), key=lambda x: x[1], reverse=True):
            output += f"  {elem}: {'█' * count} ({count}個)\n"
        
        return output
