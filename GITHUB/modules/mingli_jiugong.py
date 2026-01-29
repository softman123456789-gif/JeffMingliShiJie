#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
九宮算命分析器（生命靈數 Numerology）
基於 Pythagorean Numerology 系統
計算生命靈數、天賦數、命運數等
"""


class JiuGongAnalyzer:
    """九宮算命分析器"""
    
    def __init__(self):
        """初始化九宮分析器"""
        self.letter_values = {
            'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7, 'H': 8, 'I': 9,
            'J': 1, 'K': 2, 'L': 3, 'M': 4, 'N': 5, 'O': 6, 'P': 7, 'Q': 8, 'R': 9,
            'S': 1, 'T': 2, 'U': 3, 'V': 4, 'W': 5, 'X': 6, 'Y': 7, 'Z': 8
        }
        
        # 中文拼音對照（常用字）
        self.chinese_pinyin_map = {
            '張': 'ZHANG', '王': 'WANG', '李': 'LI', '趙': 'ZHAO', '陳': 'CHEN',
            '劉': 'LIU', '黃': 'HUANG', '周': 'ZHOU', '吳': 'WU', '徐': 'XU',
            '孫': 'SUN', '馬': 'MA', '朱': 'ZHU', '胡': 'HU', '郭': 'GUO',
            '林': 'LIN', '何': 'HE', '高': 'GAO', '梁': 'LIANG', '鄭': 'ZHENG',
            '羅': 'LUO', '宋': 'SONG', '謝': 'XIE', '唐': 'TANG', '韓': 'HAN',
            '曹': 'CAO', '許': 'XU', '鄧': 'DENG', '蕭': 'XIAO', '馮': 'FENG',
            '曾': 'ZENG', '程': 'CHENG', '蔡': 'CAI', '彭': 'PENG', '潘': 'PAN',
            '袁': 'YUAN', '于': 'YU', '董': 'DONG', '余': 'YU', '蘇': 'SU',
            '葉': 'YE', '呂': 'LV', '魏': 'WEI', '蔣': 'JIANG', '田': 'TIAN',
            '杜': 'DU', '丁': 'DING', '沈': 'SHEN', '姜': 'JIANG', '范': 'FAN',
            '江': 'JIANG', '傅': 'FU', '鐘': 'ZHONG', '盧': 'LU', '汪': 'WANG',
            '戴': 'DAI', '崔': 'CUI', '任': 'REN', '陸': 'LU', '廖': 'LIAO',
            '姚': 'YAO', '方': 'FANG', '金': 'JIN', '邱': 'QIU', '夏': 'XIA',
            '譚': 'TAN', '韋': 'WEI', '賈': 'JIA', '鄒': 'ZOU', '石': 'SHI',
            '熊': 'XIONG', '孟': 'MENG', '秦': 'QIN', '閻': 'YAN', '薛': 'XUE',
            '侯': 'HOU', '雷': 'LEI', '白': 'BAI', '龍': 'LONG', '段': 'DUAN',
            '郝': 'HAO', '孔': 'KONG', '邵': 'SHAO', '史': 'SHI', '毛': 'MAO',
            '常': 'CHANG', '萬': 'WAN', '顧': 'GU', '賴': 'LAI', '武': 'WU',
            '康': 'KANG', '文': 'WEN', '顏': 'YAN', '柳': 'LIU', '安': 'AN',
            '明': 'MING', '華': 'HUA', '國': 'GUO', '建': 'JIAN', '志': 'ZHI',
            '強': 'QIANG', '偉': 'WEI', '芳': 'FANG', '軍': 'JUN', '勇': 'YONG',
            '傑': 'JIE', '娜': 'NA', '敏': 'MIN', '靜': 'JING', '麗': 'LI',
            '秀': 'XIU', '美': 'MEI', '英': 'YING', '玲': 'LING', '婷': 'TING',
            '紅': 'HONG', '雪': 'XUE', '梅': 'MEI', '霞': 'XIA', '鳳': 'FENG',
            '雲': 'YUN', '蘭': 'LAN', '琴': 'QIN', '艷': 'YAN', '萍': 'PING',
            '佳': 'JIA', '慧': 'HUI', '瑩': 'YING', '蓉': 'RONG', '珊': 'SHAN',
            '薇': 'WEI', '倩': 'QIAN', '茹': 'RU', '莉': 'LI', '嫻': 'XIAN'
        }
    
    def get_letter_value(self, letter):
        """獲取字母的數值"""
        return self.letter_values.get(letter.upper(), 0)
    
    def reduce_to_single_digit(self, number):
        """將數字化簡為單數，保留主數字 11, 22, 33"""
        if number in [11, 22, 33]:
            return number
        
        while number > 9:
            number = sum(int(digit) for digit in str(number))
            if number in [11, 22, 33]:
                return number
        
        return number
    
    def convert_chinese_to_pinyin(self, name):
        """將中文名字轉換為拼音"""
        pinyin = ""
        for char in name:
            if char in self.chinese_pinyin_map:
                pinyin += self.chinese_pinyin_map[char]
            else:
                # 如果不在對照表中，保留原字符
                pinyin += char
        return pinyin
    
    def calculate_life_path(self, year, month, day):
        """計算生命靈數（Life Path Number）"""
        try:
            # 分別化簡年月日
            reduced_month = self.reduce_to_single_digit(month)
            reduced_day = self.reduce_to_single_digit(day)
            
            # 年份先加總再化簡
            year_sum = sum(int(digit) for digit in str(year))
            reduced_year = self.reduce_to_single_digit(year_sum)
            
            # 加總三者並化簡
            total = reduced_month + reduced_day + reduced_year
            return self.reduce_to_single_digit(total)
            
        except Exception:
            return 1
    
    def calculate_expression(self, name):
        """計算命運數（Expression Number）- 從姓名所有字母"""
        # 如果是中文名字，先轉換為拼音
        if any('\u4e00' <= char <= '\u9fff' for char in name):
            name = self.convert_chinese_to_pinyin(name)
        
        name = name.upper().replace(' ', '')
        total = sum(self.get_letter_value(letter) for letter in name if letter.isalpha())
        return self.reduce_to_single_digit(total)
    
    def calculate_soul_urge(self, name):
        """計算靈魂數（Soul Urge Number）- 從姓名母音"""
        # 如果是中文名字，先轉換為拼音
        if any('\u4e00' <= char <= '\u9fff' for char in name):
            name = self.convert_chinese_to_pinyin(name)
        
        vowels = 'AEIOU'
        name = name.upper().replace(' ', '')
        
        vowel_values = {'A': 1, 'E': 5, 'I': 9, 'O': 6, 'U': 3}
        total = sum(vowel_values.get(vowel, 0) for vowel in name if vowel in vowels)
        return self.reduce_to_single_digit(total)
    
    def calculate_personality(self, name):
        """計算個性數（Personality Number）- 從姓名子音"""
        # 如果是中文名字，先轉換為拼音
        if any('\u4e00' <= char <= '\u9fff' for char in name):
            name = self.convert_chinese_to_pinyin(name)
        
        vowels = 'AEIOU'
        name = name.upper().replace(' ', '')
        
        consonants = [letter for letter in name if letter.isalpha() and letter not in vowels]
        total = sum(self.get_letter_value(consonant) for consonant in consonants)
        return self.reduce_to_single_digit(total)
    
    def calculate_birthday_number(self, day):
        """計算生日數（Birthday Number）"""
        return self.reduce_to_single_digit(day)
    
    def get_number_meaning(self, number, number_type="life_path"):
        """獲取數字的意義"""
        meanings = {
            "life_path": {
                1: {
                    "title": "領導者",
                    "traits": "獨立、開創、自信、有主見",
                    "description": "您是天生的領袖，勇於開創新局。具有強烈的個人風格和獨立精神，不喜歡受制於人。",
                    "strength": "果斷、創新、勇氣、自信",
                    "weakness": "固執、自我、缺乏耐心",
                    "career": "適合創業、管理職、領導職位",
                    "love": "需要對方欣賞您的獨立性，給予空間"
                },
                2: {
                    "title": "和平使者",
                    "traits": "合作、外交、敏感、善解人意",
                    "description": "您天生善於調解，重視和諧。具有高度的同理心，能理解他人感受。",
                    "strength": "合作、協調、溫和、敏銳",
                    "weakness": "過於敏感、優柔寡斷、依賴",
                    "career": "適合外交、諮商、公關、團隊合作",
                    "love": "渴望穩定的伴侶關係，重視情感交流"
                },
                3: {
                    "title": "創意大師",
                    "traits": "表達、創造、樂觀、有魅力",
                    "description": "您充滿創造力和表達欲，天生的溝通者。樂觀開朗，能帶給周圍歡樂。",
                    "strength": "創意、表達、樂觀、魅力",
                    "weakness": "散漫、膚淺、情緒化",
                    "career": "適合藝術、媒體、寫作、娛樂業",
                    "love": "需要有趣、能共鳴的伴侶"
                },
                4: {
                    "title": "建設者",
                    "traits": "實際、組織、穩定、勤奮",
                    "description": "您踏實可靠，善於建立穩固基礎。重視秩序和規則，工作認真負責。",
                    "strength": "穩定、可靠、務實、組織力",
                    "weakness": "死板、保守、缺乏變通",
                    "career": "適合工程、會計、管理、建築",
                    "love": "需要穩定、忠誠的關係"
                },
                5: {
                    "title": "冒險家",
                    "traits": "自由、冒險、多變、適應力強",
                    "description": "您熱愛自由和冒險，充滿好奇心。善於適應變化，喜歡嘗試新事物。",
                    "strength": "適應力、自由、多才、活力",
                    "weakness": "不定性、衝動、缺乏耐心",
                    "career": "適合業務、旅遊、媒體、自由業",
                    "love": "需要自由空間，害怕束縛"
                },
                6: {
                    "title": "照顧者",
                    "traits": "責任、關懷、家庭、和諧",
                    "description": "您富有責任感和愛心，重視家庭和人際關係。善於照顧他人，追求和諧。",
                    "strength": "責任、關懷、和諧、治療力",
                    "weakness": "過度犧牲、控制欲、焦慮",
                    "career": "適合教育、醫護、社工、諮商",
                    "love": "重視家庭，是好伴侶和父母"
                },
                7: {
                    "title": "探索者",
                    "traits": "分析、靈性、智慧、內省",
                    "description": "您深沉內斂，喜歡思考和探索真理。具有靈性追求，重視內在成長。",
                    "strength": "智慧、分析、靈性、直覺",
                    "weakness": "孤僻、神秘、過度懷疑",
                    "career": "適合研究、教學、宗教、神秘學",
                    "love": "需要精神層面的連結"
                },
                8: {
                    "title": "成就者",
                    "traits": "權力、成功、物質、效率",
                    "description": "您具有強烈的成就動機，追求物質和權力。有商業頭腦，善於管理資源。",
                    "strength": "成就、領導、效率、商業頭腦",
                    "weakness": "物質主義、工作狂、壓力大",
                    "career": "適合商業、金融、法律、管理",
                    "love": "需要成功、有能力的伴侶"
                },
                9: {
                    "title": "人道主義者",
                    "traits": "仁慈、智慧、理想、寬容",
                    "description": "您富有同情心和理想主義，關懷世界。具有藝術天分，追求更高的人生意義。",
                    "strength": "仁慈、智慧、理想、藝術性",
                    "weakness": "不切實際、情緒化、自我犧牲",
                    "career": "適合公益、藝術、教育、慈善",
                    "love": "需要有共同理想的伴侶"
                },
                11: {
                    "title": "靈性導師（主數字）",
                    "traits": "直覺、靈感、理想、啟發",
                    "description": "您是主數字，具有特殊使命。擁有強大的直覺和靈性天賦，能啟發他人。",
                    "strength": "直覺、靈感、理想主義、啟發力",
                    "weakness": "過度敏感、緊張、不切實際",
                    "career": "適合靈性導師、藝術、心理諮商",
                    "love": "需要精神層面深度連結"
                },
                22: {
                    "title": "大建築師（主數字）",
                    "traits": "願景、實踐、建設、轉化",
                    "description": "您是主數字，能將夢想化為現實。具有實現偉大願景的能力，影響深遠。",
                    "strength": "願景、實踐力、組織力、影響力",
                    "weakness": "壓力大、要求高、控制慾",
                    "career": "適合大型企業、政治、社會改革",
                    "love": "需要能理解您使命的伴侶"
                },
                33: {
                    "title": "大師導師（主數字）",
                    "traits": "奉獻、治療、教導、愛",
                    "description": "您是最高的主數字，具有大愛和奉獻精神。能治療和教導他人，散播愛與光。",
                    "strength": "大愛、治療力、教導、奉獻",
                    "weakness": "過度犧牲、負擔過重、情緒壓力",
                    "career": "適合靈性教師、治療師、慈善事業",
                    "love": "需要能共同奉獻的靈魂伴侶"
                }
            }
        }
        
        # 其他數字類型使用相同的意義描述
        for num_type in ["expression", "soul_urge", "personality", "birthday"]:
            meanings[num_type] = meanings["life_path"]
        
        return meanings.get(number_type, {}).get(number, meanings[number_type][1])
    
    def analyze_jiugong(self, name, year, month, day):
        """進行完整的九宮分析"""
        try:
            # 計算各種數字
            life_path = self.calculate_life_path(year, month, day)
            expression = self.calculate_expression(name)
            soul_urge = self.calculate_soul_urge(name)
            personality = self.calculate_personality(name)
            birthday = self.calculate_birthday_number(day)
            
            # 生成分析報告
            report = self._generate_report(name, year, month, day, 
                                          life_path, expression, soul_urge, 
                                          personality, birthday)
            
            return report
            
        except Exception as e:
            return f"九宮分析出現錯誤：{str(e)}"
    
    def _generate_report(self, name, year, month, day, 
                        life_path, expression, soul_urge, personality, birthday):
        """生成分析報告"""
        
        # 取得各數字的意義
        lp_meaning = self.get_number_meaning(life_path, "life_path")
        exp_meaning = self.get_number_meaning(expression, "expression")
        su_meaning = self.get_number_meaning(soul_urge, "soul_urge")
        per_meaning = self.get_number_meaning(personality, "personality")
        bd_meaning = self.get_number_meaning(birthday, "birthday")
        
        report = f"""
{'='*80}
                    🔢 九宮算命分析報告（生命靈數）🔢
{'='*80}

【基本資料】
姓名：{name}
出生日期：{year}年{month}月{day}日

{'='*80}
                          核心數字總覽
{'='*80}

┌─────────────────────────────────────────────────────┐
│ 🌟 生命靈數（Life Path）： {life_path}                    │
│    【{lp_meaning['title']}】                           │
│    這是您的人生道路和主要使命                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 💫 命運數（Expression）： {expression}                   │
│    【{exp_meaning['title']}】                          │
│    這是您的天賦才能和人生目標                            │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ ❤ 靈魂數（Soul Urge）： {soul_urge}                     │
│    【{su_meaning['title']}】                           │
│    這是您內心的渴望和動機                               │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 👤 個性數（Personality）： {personality}                │
│    【{per_meaning['title']}】                          │
│    這是他人眼中的您                                     │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│ 🎂 生日數（Birthday）： {birthday}                      │
│    【{bd_meaning['title']}】                           │
│    這是您的特殊天賦                                     │
└─────────────────────────────────────────────────────┘

{'='*80}
                        詳細解析
{'='*80}

【生命靈數 {life_path} - {lp_meaning['title']}】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✦ 核心特質：{lp_meaning['traits']}

✦ 總體描述：
{lp_meaning['description']}

✦ 主要優勢：
{lp_meaning['strength']}

✦ 需要注意：
{lp_meaning['weakness']}

✦ 事業建議：
{lp_meaning['career']}

✦ 感情特質：
{lp_meaning['love']}

{'─'*80}

【命運數 {expression} - {exp_meaning['title']}】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✦ 天賦才能：{exp_meaning['traits']}

✦ 人生使命：
您的姓名蘊含著{expression}號的能量，代表{exp_meaning['description']}

✦ 發展方向：
{exp_meaning['career']}

{'─'*80}

【靈魂數 {soul_urge} - {su_meaning['title']}】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✦ 內心渴望：{su_meaning['traits']}

✦ 真實自我：
{su_meaning['description']}

✦ 心靈需求：
{su_meaning['love']}

{'─'*80}

【個性數 {personality} - {per_meaning['title']}】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✦ 外在表現：{per_meaning['traits']}

✦ 他人印象：
{per_meaning['description']}

✦ 社交風格：
{per_meaning['strength']}

{'─'*80}

【生日數 {birthday} - {bd_meaning['title']}】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

✦ 特殊天賦：{bd_meaning['traits']}

✦ 天賦能力：
生日數{birthday}賦予您{bd_meaning['description']}

{'='*80}
                        九宮格能量分布
{'='*80}

{self._generate_grid(name, year, month, day)}

{'='*80}
                        總結與建議
{'='*80}

【整體評估】
根據您的九宮數字分析：

✦ 生命方向：生命靈數{life_path}指引您成為{lp_meaning['title']}，
  這是您的人生主要方向。

✦ 發揮天賦：命運數{expression}顯示您具有{exp_meaning['title']}的特質，
  善用這些天賦將幫助您實現人生目標。

✦ 平衡內外：您的靈魂渴望({su_meaning['title']})與外在表現
  ({per_meaning['title']})需要取得平衡。

✦ 特殊能力：生日數{birthday}是您的特殊禮物，記得善加運用。

【開運建議】
1. 接納自己的{lp_meaning['title']}特質，順勢而為
2. 發展{exp_meaning['career']}方面的才能
3. 注意{lp_meaning['weakness']}的傾向，適時調整
4. 在感情中{lp_meaning['love']}

願九宮靈數的智慧指引您的人生旅程！ 🌟

{'='*80}
"""
        return report
    
    def _generate_grid(self, name, year, month, day):
        """生成九宮格能量分布圖"""
        # 計算姓名和生日中各數字出現的次數
        all_numbers = []
        
        # 從姓名計算
        if any('\u4e00' <= char <= '\u9fff' for char in name):
            name = self.convert_chinese_to_pinyin(name)
        name = name.upper().replace(' ', '')
        for letter in name:
            if letter.isalpha():
                value = self.get_letter_value(letter)
                if 1 <= value <= 9:
                    all_numbers.append(value)
        
        # 從生日計算
        date_str = f"{year}{month:02d}{day:02d}"
        for digit in date_str:
            if digit != '0':
                all_numbers.append(int(digit))
        
        # 統計1-9出現次數
        count = {i: all_numbers.count(i) for i in range(1, 10)}
        
        # 生成九宮格圖
        grid = f"""
        ┌─────────┬─────────┬─────────┐
        │    3    │    6    │    9    │
        │  {self._format_count(count[3])}  │  {self._format_count(count[6])}  │  {self._format_count(count[9])}  │
        │ (創意)  │ (責任)  │ (智慧)  │
        ├─────────┼─────────┼─────────┤
        │    2    │    5    │    8    │
        │  {self._format_count(count[2])}  │  {self._format_count(count[5])}  │  {self._format_count(count[8])}  │
        │ (合作)  │ (自由)  │ (力量)  │
        ├─────────┼─────────┼─────────┤
        │    1    │    4    │    7    │
        │  {self._format_count(count[1])}  │  {self._format_count(count[4])}  │  {self._format_count(count[7])}  │
        │ (領導)  │ (穩定)  │ (靈性)  │
        └─────────┴─────────┴─────────┘

能量解讀：
• 數字 1 ({count[1]}次) - 領導與獨立能量
• 數字 2 ({count[2]}次) - 合作與外交能量
• 數字 3 ({count[3]}次) - 創意與表達能量
• 數字 4 ({count[4]}次) - 穩定與務實能量
• 數字 5 ({count[5]}次) - 自由與冒險能量
• 數字 6 ({count[6]}次) - 責任與關懷能量
• 數字 7 ({count[7]}次) - 靈性與智慧能量
• 數字 8 ({count[8]}次) - 權力與成就能量
• 數字 9 ({count[9]}次) - 完成與智慧能量

能量平衡：
{self._analyze_grid_balance(count)}
"""
        return grid
    
    def _format_count(self, count):
        """格式化數字計數顯示"""
        if count == 0:
            return "  -  "
        elif count <= 3:
            return "●" * count + "  "
        else:
            return "●●●+"
    
    def _analyze_grid_balance(self, count):
        """分析九宮格能量平衡"""
        analysis = []
        
        # 檢查缺失的數字
        missing = [i for i in range(1, 10) if count[i] == 0]
        if missing:
            analysis.append(f"✦ 缺少數字：{', '.join(map(str, missing))} - 這些領域需要額外培養")
        
        # 檢查過多的數字
        excessive = [i for i in range(1, 10) if count[i] >= 4]
        if excessive:
            analysis.append(f"✦ 能量過強：{', '.join(map(str, excessive))} - 需要適度平衡")
        
        # 檢查平衡的數字
        balanced = [i for i in range(1, 10) if 1 <= count[i] <= 3]
        if balanced:
            analysis.append(f"✦ 平衡能量：{', '.join(map(str, balanced))} - 發展良好")
        
        if not analysis:
            analysis.append("✦ 整體能量分布均衡")
        
        return "\n".join(analysis)


# 測試函數
if __name__ == "__main__":
    analyzer = JiuGongAnalyzer()
    
    # 測試中文姓名
    result = analyzer.analyze_jiugong("王小明", 1990, 5, 15)
    print(result)
