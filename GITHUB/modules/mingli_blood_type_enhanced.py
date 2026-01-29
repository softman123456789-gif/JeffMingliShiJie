#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
血型命理模組增強版
集成 https://github.com/alangprs/bloodType 的遺傳邏輯
包含血型性格分析和血型遺傳計算
"""

from typing import Dict, List, Tuple


class BloodTypeAnalyzerEnhanced:
    """增強的血型分析 - 包含性格分析和遺傳計算"""
    
    BLOOD_TYPES = {
        'A': {
            'name': 'A 型',
            'symbol': 'A',
            'personality': '慎重、內向、守規則。A 型人性格認真謹慎，做事按部就班，注重團隊和諧。',
            'traits': ['慎重', '認真', '守規則', '內向', '體貼'],
            'strengths': ['責任感強', '工作認真', '忠誠度高', '考慮周周', '團隊意識強'],
            'weaknesses': ['過於謹慎', '容易焦慮', '缺乏變通', '表達困難', '優柔寡斷'],
            'suitable_careers': ['會計師', '教師', '醫生', '律師', '公務員'],
            'lucky_color': '綠色',
            'lucky_number': 7,
        },
        'B': {
            'name': 'B 型',
            'symbol': 'B',
            'personality': '熱情、開朗、我行我素。B 型人性格開朗熱情，做事靈活變通，但有時自我中心。',
            'traits': ['熱情', '開朗', '靈活', '自由', '創意'],
            'strengths': ['樂觀積極', '適應快', '創新精神', '社交能力強', '行動力強'],
            'weaknesses': ['缺乏耐心', '易衝動', '不夠細心', '自我中心', '不穩定'],
            'suitable_careers': ['創業者', '營銷人員', '演藝人員', '運動員', '設計師'],
            'lucky_color': '紅色',
            'lucky_number': 9,
        },
        'AB': {
            'name': 'AB 型',
            'symbol': 'AB',
            'personality': '冷靜、理性、神祕。AB 型人兼具 A 型和 B 型特徵，既有理性也有感性，較難捉摸。',
            'traits': ['冷靜', '理性', '神祕', '雙重性格', '獨特'],
            'strengths': ['分析能力強', '適應快', '創新思維', '做決定快', '獨立思考'],
            'weaknesses': ['難以親近', '不穩定', '自我評價低', '易多疑', '缺乏親和力'],
            'suitable_careers': ['研究員', '程式設計師', '分析師', '藝術家', '顧問'],
            'lucky_color': '紫色',
            'lucky_number': 4,
        },
        'O': {
            'name': 'O 型',
            'symbol': 'O',
            'personality': '活潑、社交、領導力強。O 型人性格活潑開朗，領導力強，人氣旺，是天生的領導者。',
            'traits': ['活潑', '開朗', '領導力', '社交', '樂觀'],
            'strengths': ['領導力強', '社交能力強', '樂觀積極', '親和力好', '做事果斷'],
            'weaknesses': ['過於自信', '容易驕傲', '不夠細心', '易衝動', '缺乏耐心'],
            'suitable_careers': ['管理層', '銷售', '政治人物', '運動員', '主持人'],
            'lucky_color': '黃色',
            'lucky_number': 1,
        }
    }
    
    def __init__(self):
        """初始化血型分析器"""
        pass
    
    def analyze_blood_type(self, blood_type: str) -> str:
        """分析血型性格"""
        bt = self.BLOOD_TYPES.get(blood_type.upper(), self.BLOOD_TYPES['O'])
        
        result = f"""
【{bt['symbol']} {bt['name']} 血型分析】

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
    
    def _get_compatibility(self, type1: str, type2: str) -> str:
        """獲取血型相容性"""
        compatibility_matrix = {
            ('A', 'A'): '100% - 志同道合',
            ('A', 'B'): '60% - 互補但需理解',
            ('A', 'AB'): '90% - 相當相容',
            ('A', 'O'): '70% - 基本和諧',
            ('B', 'A'): '60% - 互補但需理解',
            ('B', 'B'): '100% - 志同道合',
            ('B', 'AB'): '80% - 相當相容',
            ('B', 'O'): '90% - 相當相容',
            ('AB', 'A'): '90% - 相當相容',
            ('AB', 'B'): '80% - 相當相容',
            ('AB', 'AB'): '100% - 志同道合',
            ('AB', 'O'): '70% - 基本和諧',
            ('O', 'A'): '70% - 基本和諧',
            ('O', 'B'): '90% - 相當相容',
            ('O', 'AB'): '70% - 基本和諧',
            ('O', 'O'): '100% - 志同道合',
        }
        
        key = (type1.upper(), type2.upper())
        return compatibility_matrix.get(key, '70% - 基本和諧')
    
    def predict_baby_blood_type(self, parent1_blood: str, parent2_blood: str) -> str:
        """預測小孩可能的血型（基於 GitHub 項目邏輯）
        
        血型遺傳規律:
        - A 型 = AA 或 AO
        - B 型 = BB 或 BO
        - AB 型 = AB
        - O 型 = OO
        """
        p1 = parent1_blood.upper()
        p2 = parent2_blood.upper()
        
        # 將血型轉換為基因
        parent1_genes = self._blood_type_to_genes(p1)
        parent2_genes = self._blood_type_to_genes(p2)
        
        # 計算所有可能的組合
        possible_babies = set()
        
        for g1 in parent1_genes:
            for g2 in parent2_genes:
                # 小孩的基因組合
                baby_genes = tuple(sorted([g1, g2]))
                # 轉換為血型
                baby_blood = self._genes_to_blood_type(baby_genes)
                possible_babies.add(baby_blood)
        
        result = f"""
【血型遺傳預測】

父親血型: {p1} 型
母親血型: {p2} 型

═════════════════════════════

小孩可能的血型:
  {', '.join(sorted(possible_babies))}

遺傳説明:
  血型由父母各提供一個基因決定
  - A 型由 AA 或 AO 組成
  - B 型由 BB 或 BO 組成
  - AB 型由 AB 組成
  - O 型由 OO 組成

【遺傳機率分析】
"""
        
        # 計算每種血型的機率
        blood_count = {}
        total = 0
        for g1 in parent1_genes:
            for g2 in parent2_genes:
                baby_genes = tuple(sorted([g1, g2]))
                baby_blood = self._genes_to_blood_type(baby_genes)
                blood_count[baby_blood] = blood_count.get(baby_blood, 0) + 1
                total += 1
        
        for blood, count in sorted(blood_count.items()):
            probability = (count / total) * 100
            result += f"\n  {blood} 型: {probability:.1f}% ({count}/{total})"
        
        result += "\n"
        return result
    
    def _blood_type_to_genes(self, blood_type: str) -> List[str]:
        """將血型轉換為可能的基因組合"""
        blood_type = blood_type.upper()
        if blood_type == 'A':
            return ['A', 'A', 'A', 'O']  # AA 或 AO (各 50% 概率)
        elif blood_type == 'B':
            return ['B', 'B', 'B', 'O']  # BB 或 BO (各 50% 概率)
        elif blood_type == 'AB':
            return ['A', 'B']  # 只能是 AB
        elif blood_type == 'O':
            return ['O', 'O']  # 只能是 OO
        return ['O', 'O']
    
    def _genes_to_blood_type(self, genes: Tuple[str, str]) -> str:
        """將基因組合轉換為血型"""
        g1, g2 = genes
        
        if g1 == 'A' and g2 == 'A':
            return 'A'
        elif g1 == 'A' and g2 == 'B':
            return 'AB'
        elif g1 == 'B' and g2 == 'B':
            return 'B'
        elif g1 == 'O' and g2 == 'O':
            return 'O'
        elif g1 == 'A' and g2 == 'O':
            return 'A'
        elif g1 == 'B' and g2 == 'O':
            return 'B'
        else:
            return 'O'


def test_blood_type_enhanced():
    """測試增強的血型模組"""
    print("【血型分析測試】\n")
    
    analyzer = BloodTypeAnalyzerEnhanced()
    
    # 測試性格分析
    print(analyzer.analyze_blood_type('O'))
    
    # 測試遺傳預測
    print("\n" + "="*60)
    print(analyzer.predict_baby_blood_type('A', 'B'))
    
    # 更多遺傳預測例子
    test_cases = [
        ('A', 'A'),
        ('B', 'B'),
        ('AB', 'O'),
        ('O', 'O'),
    ]
    
    for p1, p2 in test_cases:
        print(analyzer.predict_baby_blood_type(p1, p2))


if __name__ == '__main__':
    test_blood_type_enhanced()
