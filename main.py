#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jeff命理世界 - Android App
將 Windows 桌面版轉換為 Android 移動應用
使用 Kivy 框架
"""

import os
import sys
from pathlib import Path

# 設定路徑
BASE_PATH = Path(__file__).parent
MODULES_PATH = BASE_PATH / 'GITHUB' / 'modules'
GITHUB_PATH = BASE_PATH / 'GITHUB'

# 添加路徑到 sys.path
if MODULES_PATH.exists():
    sys.path.insert(0, str(MODULES_PATH))
if GITHUB_PATH.exists():
    sys.path.insert(0, str(GITHUB_PATH))

# 匯入命理模組
try:
    from mingli_astrology import ZodiacSignAnalyzer
    from mingli_blood_type_enhanced import BloodTypeAnalyzer
    from mingli_bazi_analyzer import BaziAnalyzer
    from mingli_purplestar_analyzer import PurpleStarAnalyzer
    from mingli_tarot import TarotAnalyzer
    from mingli_yijing import YijingAnalyzer
    from mingli_jiugong import JiuGongAnalyzer
    from mingli_jiugong_name_enhanced import JiuGongNameAnalyzerEnhanced
    from spouse_compatibility_professional import ProfessionalSpouseCompatibilityAnalyzer
    print("[OK] 所有命理模組載入成功")
except ImportError as e:
    print(f"[WARNING] 模組載入失敗: {e}")

from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.image import Image as KivyImage
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.core.window import Window
from datetime import datetime

# 設定視窗大小（適配手機螢幕）
Window.size = (1080, 1920)


class JiuGongAnalysisScreen:
    """九宮分析功能"""
    def __init__(self):
        self.analyzer = JiuGongAnalyzer()
    
    def analyze(self, name):
        """進行九宮分析"""
        return self.analyzer.analyze(name)


class AstrologyAnalysisScreen:
    """星座分析功能"""
    def __init__(self):
        self.analyzer = ZodiacSignAnalyzer()
    
    def analyze(self, birth_date, name):
        """進行星座分析"""
        return self.analyzer.analyze(birth_date, name)


class BaziAnalysisScreen:
    """八字分析功能"""
    def __init__(self):
        self.analyzer = BaziAnalyzer()
    
    def analyze(self, year, month, day, hour):
        """進行八字分析"""
        return self.analyzer.analyze(year, month, day, hour)


class MainApp(App):
    """主應用程式類"""
    
    def build(self):
        """建立應用介面"""
        self.title = 'Jeff命理世界 - Android版'
        
        # 主容器
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 標題
        title_label = Label(
            text='[b]Jeff命理世界 v6.7[/b]\n命理分析系統',
            size_hint_y=0.1,
            markup=True,
            font_size='24sp'
        )
        main_layout.add_widget(title_label)
        
        # 功能按鈕區
        button_layout = GridLayout(cols=2, spacing=10, size_hint_y=0.3)
        
        # 功能按鈕
        buttons = [
            ('九宮分析', self.open_jiugong),
            ('星座分析', self.open_astrology),
            ('八字分析', self.open_bazi),
            ('紫微分析', self.open_purplestar),
            ('塔羅牌', self.open_tarot),
            ('周易卜卦', self.open_yijing),
            ('配偶合適性', self.open_spouse),
            ('名字分析', self.open_name_analysis),
        ]
        
        for btn_text, btn_func in buttons:
            btn = Button(
                text=btn_text,
                size_hint_y=None,
                height=60,
                font_size='18sp'
            )
            btn.bind(on_press=btn_func)
            button_layout.add_widget(btn)
        
        main_layout.add_widget(button_layout)
        
        # 結果顯示區
        self.result_scroll = ScrollView(size_hint_y=0.6)
        self.result_label = Label(
            text='選擇功能進行分析...',
            markup=True,
            size_hint_y=None
        )
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_scroll.add_widget(self.result_label)
        main_layout.add_widget(self.result_scroll)
        
        return main_layout
    
    def show_result(self, title, content):
        """顯示分析結果"""
        result_text = f'[b]{title}[/b]\n\n{content}'
        self.result_label.text = result_text
    
    def open_jiugong(self, instance):
        """開啟九宮分析"""
        self.show_result('九宮分析', '請輸入您的姓名進行九宮分析...')
    
    def open_astrology(self, instance):
        """開啟星座分析"""
        self.show_result('星座分析', '請輸入您的出生日期進行星座分析...')
    
    def open_bazi(self, instance):
        """開啟八字分析"""
        self.show_result('八字分析', '請輸入您的出生年月日時進行八字分析...')
    
    def open_purplestar(self, instance):
        """開啟紫微分析"""
        self.show_result('紫微分析', '請輸入必要資訊進行紫微分析...')
    
    def open_tarot(self, instance):
        """開啟塔羅牌"""
        self.show_result('塔羅牌', '請選擇塔羅牌卜卦方式...')
    
    def open_yijing(self, instance):
        """開啟周易卜卦"""
        self.show_result('周易卜卦', '請進行周易卜卦...')
    
    def open_spouse(self, instance):
        """開啟配偶合適性分析"""
        self.show_result('配偶合適性', '請輸入雙方資訊進行合適性分析...')
    
    def open_name_analysis(self, instance):
        """開啟名字分析"""
        self.show_result('名字分析', '請輸入姓名進行詳細分析...')


if __name__ == '__main__':
    app = MainApp()
    app.run()
