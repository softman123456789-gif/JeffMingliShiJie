#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
星座和血型命理模組
包含十二星座分析和血型性格分析
"""

from datetime import datetime
from typing import Tuple, Dict, List


class ZodiacSignAnalyzer:
    """十二星座分析"""
    
    ZODIAC_SIGNS = [
        {
            'name': '白羊座',
            'en_name': 'Aries',
            'symbol': '♈',
            'date_range': '3月21日-4月19日',
            'element': '火',
            'ruling_planet': '火星',
            'color': '紅色',
            'lucky_number': 6,
            'traits': ['勇敢', '熱情', '直率', '衝動', '領導力'],
            'compatible': ['獅子座', '射手座', '白羊座'],
            'incompatible': ['巨蟹座', '天秤座', '摩羯座'],
        },
        {
            'name': '金牛座',
            'en_name': 'Taurus',
            'symbol': '♉',
            'date_range': '4月20日-5月20日',
            'element': '土',
            'ruling_planet': '金星',
            'color': '綠色',
            'lucky_number': 2,
            'traits': ['穩定', '實際', '忠誠', '固執', '務實'],
            'compatible': ['處女座', '摩羯座', '金牛座'],
            'incompatible': ['獅子座', '天蝎座', '水瓶座'],
        },
        {
            'name': '雙子座',
            'en_name': 'Gemini',
            'symbol': '♊',
            'date_range': '5月21日-6月20日',
            'element': '風',
            'ruling_planet': '水星',
            'color': '黃色',
            'lucky_number': 5,
            'traits': ['聰慧', '多才', '靈活', '不安', '好奇'],
            'compatible': ['天秤座', '水瓶座', '雙子座'],
            'incompatible': ['射手座', '雙魚座', '處女座'],
        },
        {
            'name': '巨蟹座',
            'en_name': 'Cancer',
            'symbol': '♋',
            'date_range': '6月21日-7月22日',
            'element': '水',
            'ruling_planet': '月亮',
            'color': '銀色',
            'lucky_number': 2,
            'traits': ['敏感', '溫柔', '家庭至上', '情緒化', '保護欲強'],
            'compatible': ['天蝎座', '雙魚座', '巨蟹座'],
            'incompatible': ['白羊座', '天秤座', '摩羯座'],
        },
        {
            'name': '獅子座',
            'en_name': 'Leo',
            'symbol': '♌',
            'date_range': '7月23日-8月22日',
            'element': '火',
            'ruling_planet': '太陽',
            'color': '金色',
            'lucky_number': 1,
            'traits': ['自信', '大方', '熱心', '驕傲', '領導力'],
            'compatible': ['白羊座', '射手座', '獅子座'],
            'incompatible': ['金牛座', '天蝎座', '水瓶座'],
        },
        {
            'name': '處女座',
            'en_name': 'Virgo',
            'symbol': '♍',
            'date_range': '8月23日-9月22日',
            'element': '土',
            'ruling_planet': '水星',
            'color': '綠色',
            'lucky_number': 5,
            'traits': ['完美主義', '聰慧', '謹慎', '挑剔', '實用'],
            'compatible': ['金牛座', '摩羯座', '處女座'],
            'incompatible': ['雙子座', '射手座', '雙魚座'],
        },
        {
            'name': '天秤座',
            'en_name': 'Libra',
            'symbol': '♎',
            'date_range': '9月23日-10月22日',
            'element': '風',
            'ruling_planet': '金星',
            'color': '藍色',
            'lucky_number': 6,
            'traits': ['和諧', '公正', '優雅', '猶豫', '交際'],
            'compatible': ['雙子座', '水瓶座', '天秤座'],
            'incompatible': ['白羊座', '巨蟹座', '摩羯座'],
        },
        {
            'name': '天蠍座',
            'en_name': 'Scorpio',
            'symbol': '♏',
            'date_range': '10月23日-11月21日',
            'element': '水',
            'ruling_planet': '冥王星',
            'color': '深紅色',
            'lucky_number': 8,
            'traits': ['神秘', '熱情', '意志強', '獨佔欲強', '深邃'],
            'compatible': ['巨蟹座', '雙魚座', '天蠍座'],
            'incompatible': ['金牛座', '獅子座', '水瓶座'],
        },
        {
            'name': '射手座',
            'en_name': 'Sagittarius',
            'symbol': '♐',
            'date_range': '11月22日-12月21日',
            'element': '火',
            'ruling_planet': '木星',
            'color': '紫色',
            'lucky_number': 9,
            'traits': ['樂觀', '自由', '誠實', '冒險', '哲學思維'],
            'compatible': ['白羊座', '獅子座', '射手座'],
            'incompatible': ['雙子座', '處女座', '雙魚座'],
        },
        {
            'name': '摩羯座',
            'en_name': 'Capricorn',
            'symbol': '♑',
            'date_range': '12月22日-1月19日',
            'element': '土',
            'ruling_planet': '土星',
            'color': '黑色',
            'lucky_number': 8,
            'traits': ['實際', '堅毅', '野心勃勃', '冷淡', '職責心強'],
            'compatible': ['金牛座', '處女座', '摩羯座'],
            'incompatible': ['白羊座', '巨蟹座', '天秤座'],
        },
        {
            'name': '水瓶座',
            'en_name': 'Aquarius',
            'symbol': '♒',
            'date_range': '1月20日-2月18日',
            'element': '風',
            'ruling_planet': '天王星',
            'color': '青色',
            'lucky_number': 4,
            'traits': ['獨立', '聰慧', '人道主義', '古怪', '前衛'],
            'compatible': ['雙子座', '天秤座', '水瓶座'],
            'incompatible': ['金牛座', '獅子座', '天蝎座'],
        },
        {
            'name': '雙魚座',
            'en_name': 'Pisces',
            'symbol': '♓',
            'date_range': '2月19日-3月20日',
            'element': '水',
            'ruling_planet': '海王星',
            'color': '海綠色',
            'lucky_number': 7,
            'traits': ['溫柔', '藝術', '同情心', '幻想', '敏感'],
            'compatible': ['巨蟹座', '天蝎座', '雙魚座'],
            'incompatible': ['雙子座', '射手座', '處女座'],
        }
    ]
    
    def __init__(self):
        self.signs = {sign['name']: sign for sign in self.ZODIAC_SIGNS}
    
    def get_zodiac_by_date(self, month: int, day: int) -> Dict:
        """根據月日獲取星座"""
        # 白羊座: 3/21-4/19
        if (month == 3 and day >= 21) or (month == 4 and day <= 19):
            return self.ZODIAC_SIGNS[0]
        # 金牛座: 4/20-5/20
        elif (month == 4 and day >= 20) or (month == 5 and day <= 20):
            return self.ZODIAC_SIGNS[1]
        # 雙子座: 5/21-6/20
        elif (month == 5 and day >= 21) or (month == 6 and day <= 20):
            return self.ZODIAC_SIGNS[2]
        # 巨蟹座: 6/21-7/22
        elif (month == 6 and day >= 21) or (month == 7 and day <= 22):
            return self.ZODIAC_SIGNS[3]
        # 獅子座: 7/23-8/22
        elif (month == 7 and day >= 23) or (month == 8 and day <= 22):
            return self.ZODIAC_SIGNS[4]
        # 處女座: 8/23-9/22
        elif (month == 8 and day >= 23) or (month == 9 and day <= 22):
            return self.ZODIAC_SIGNS[5]
        # 天秤座: 9/23-10/22
        elif (month == 9 and day >= 23) or (month == 10 and day <= 22):
            return self.ZODIAC_SIGNS[6]
        # 天蠍座: 10/23-11/21
        elif (month == 10 and day >= 23) or (month == 11 and day <= 21):
            return self.ZODIAC_SIGNS[7]
        # 射手座: 11/22-12/21
        elif (month == 11 and day >= 22) or (month == 12 and day <= 21):
            return self.ZODIAC_SIGNS[8]
        # 摩羯座: 12/22-1/19
        elif (month == 12 and day >= 22) or (month == 1 and day <= 19):
            return self.ZODIAC_SIGNS[9]
        # 水瓶座: 1/20-2/18
        elif (month == 1 and day >= 20) or (month == 2 and day <= 18):
            return self.ZODIAC_SIGNS[10]
        # 雙魚座: 2/19-3/20
        elif (month == 2 and day >= 19) or (month == 3 and day <= 20):
            return self.ZODIAC_SIGNS[11]
        
        return self.ZODIAC_SIGNS[0]  # 默認返回白羊座
    
    def analyze_zodiac(self, month: int, day: int) -> str:
        """分析星座信息"""
        sign = self.get_zodiac_by_date(month, day)
        
        result = f"""
【{sign['symbol']} {sign['name']} 星座分析】

基本信息:
  英文名: {sign['en_name']}
  日期: {sign['date_range']}
  元素: {sign['element']}
  守護星: {sign['ruling_planet']}
  幸運色: {sign['color']}
  幸運數字: {sign['lucky_number']}

性格特點:
  {', '.join(sign['traits'])}

愛情相容性:
  ✓ 最配: {', '.join(sign['compatible'])}
  ✗ 衝突: {', '.join(sign['incompatible'])}

運勢提示:
  本月運勢整體向好，{sign['ruling_planet']}帶來積極影響。
  建議多與{sign['compatible'][0]}座的人交往，增進理解。
  避免與{sign['incompatible'][0]}座發生衝突。

日期範圍: {sign['date_range']}
        """
        
        return result
    
    def get_all_signs(self) -> List[Dict]:
        """獲取所有星座"""
        return self.ZODIAC_SIGNS


class BloodTypeAnalyzer:
    """血型分析"""
    
    BLOOD_TYPES = {
        'A': {
            'name': 'A 型血',
            'traits': ['謹慎', '認真', '完美主義', '保守', '可靠'],
            'personality': '細心謹慎，很在乎他人的看法，具有強烈的責任感。',
            'strengths': ['認真負責', '細心周密', '遵守紀律', '忠誠可靠'],
            'weaknesses': ['過度謹慎', '固執保守', '容易緊張', '難以變通'],
            'suitable_careers': ['會計師', '工程師', '教師', '醫生', '律師'],
            'lucky_color': '綠色',
            'lucky_number': 1,
        },
        'B': {
            'name': 'B 型血',
            'traits': ['活潑', '樂觀', '靈活', '冒險', '社交能力強'],
            'personality': '積極樂觀，喜歡交朋友，適應能力強，有創新精神。',
            'strengths': ['樂觀開朗', '社交能力強', '適應力強', '創新思維'],
            'weaknesses': ['缺乏耐心', '容易任性', '不夠細心', '淺嘗即止'],
            'suitable_careers': ['銷售', '藝術家', '創業者', '主持人', '設計師'],
            'lucky_color': '紅色',
            'lucky_number': 9,
        },
        'AB': {
            'name': 'AB 型血',
            'traits': ['理性', '聰慧', '雙重性格', '獨特', '冷靜'],
            'personality': '具有理性與感性的雙重性格，聰慧冷靜，但有些情緒化。',
            'strengths': ['理性聰慧', '判斷力強', '獨立思考', '神秘魅力'],
            'weaknesses': ['情緒不穩定', '難以相處', '過度理性', '自我中心'],
            'suitable_careers': ['科學家', '分析師', '藝術家', '諮詢師', '研究員'],
            'lucky_color': '紫色',
            'lucky_number': 5,
        },
        'O': {
            'name': 'O 型血',
            'traits': ['熱血', '直率', '領導力', '開朗', '勇敢'],
            'personality': '開朗熱血，有領導才能，性格直率，喜歡冒險。',
            'strengths': ['領導力強', '開朗熱血', '勇敢直率', '親和力強'],
            'weaknesses': ['有時專制', '易衝動', '缺乏細節觀察', '固執己見'],
            'suitable_careers': ['管理層', '運動員', '軍人', '消防員', '企業家'],
            'lucky_color': '黃色',
            'lucky_number': 3,
        }
    }
    
    def analyze_blood_type(self, blood_type: str) -> str:
        """分析血型性格"""
        bt = self.BLOOD_TYPES.get(blood_type.upper(), self.BLOOD_TYPES['O'])
        
        result = f"""
【{bt['name']} 血型分析】

性格描述:
  {bt['personality']}

主要特點:
  {', '.join(bt['traits'])}

優勢:
  ✓ {', '.join(bt['strengths'])}

劣勢:
  ✗ {', '.join(bt['weaknesses'])}

適合職業:
  {', '.join(bt['suitable_careers'])}

幸運信息:
  幸運色: {bt['lucky_color']}
  幸運數字: {bt['lucky_number']}

與其他血型的相容性:
  與 A 型血: {self._get_compatibility(blood_type, 'A')}
  與 B 型血: {self._get_compatibility(blood_type, 'B')}
  與 AB 型血: {self._get_compatibility(blood_type, 'AB')}
  與 O 型血: {self._get_compatibility(blood_type, 'O')}

建議:
  根據{bt['name']}的特性，建議多參加社交活動，
  充分發揮自身優勢，同時要注意克服劣勢。
        """
        
        return result
    
    def _get_compatibility(self, type1: str, type2: str) -> int:
        """獲取血型相容性百分比"""
        # 簡化的相容性分析（返回百分比數字）
        compatibility_matrix = {
            ('A', 'A'): 100,
            ('A', 'B'): 60,
            ('A', 'AB'): 90,
            ('A', 'O'): 70,
            ('B', 'A'): 60,
            ('B', 'B'): 100,
            ('B', 'AB'): 80,
            ('B', 'O'): 90,
            ('AB', 'A'): 90,
            ('AB', 'B'): 80,
            ('AB', 'AB'): 100,
            ('AB', 'O'): 70,
            ('O', 'A'): 70,
            ('O', 'B'): 90,
            ('O', 'AB'): 70,
            ('O', 'O'): 100,
        }
        
        key = (type1.upper(), type2.upper())
        compat_score = compatibility_matrix.get(key, 70)
        
        # 返回格式化字符串用於顯示
        descriptions = {
            100: '100% - 志同道合',
            90: '90% - 相當相容',
            80: '80% - 相當相容',
            70: '70% - 基本和諧',
            60: '60% - 互補但需理解',
        }
        
        return descriptions.get(compat_score, '70% - 基本和諧')


def test_astrology():
    """測試星座模組"""
    print("【星座模組測試】\n")
    
    zodiac = ZodiacSignAnalyzer()
    
    # 測試星座分析
    print(zodiac.analyze_zodiac(3, 21))  # 白羊座
    print(zodiac.analyze_zodiac(7, 23))  # 獅子座
    
    print("\n【血型模組測試】\n")
    
    blood = BloodTypeAnalyzer()
    
    # 測試血型分析
    print(blood.analyze_blood_type('A'))
    print(blood.analyze_blood_type('O'))


if __name__ == '__main__':
    test_astrology()
