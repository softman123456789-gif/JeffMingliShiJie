#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Jeff命理世界 - Kivy Android App (增強版)
將 Windows 桌面版完全轉換為 Android 應用
"""

import os
import sys
from pathlib import Path
from datetime import datetime
from functools import partial

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
    try:
        from spouse_compatibility_professional import ProfessionalSpouseCompatibilityAnalyzer
    except:
        ProfessionalSpouseCompatibilityAnalyzer = None
    print("[OK] 所有命理模組載入成功")
except ImportError as e:
    print(f"[WARNING] 模組載入失敗: {e}")

# Kivy 匯入
from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.scrollview import ScrollView
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.spinner import Spinner
from kivy.uix.textinput import TextInput
from kivy.uix.popup import Popup
from kivy.uix.filechooser import FileChooserListView
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.core.window import Window
from kivy.uix.image import Image as KivyImage
from kivy.garden.matplotlib.backend_kivyagg import FigureCanvasKivyAgg
from kivy.metrics import dp

# 設定視窗大小（適配手機螢幕）
Window.size = (1080, 1920)


class JiuGongScreen(Screen):
    """九宮分析螢幕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzer = JiuGongAnalyzer()
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # 標題
        title = Label(text='[b]九宮分析[/b]', size_hint_y=0.1, markup=True, font_size='24sp')
        layout.add_widget(title)
        
        # 輸入區
        input_layout = BoxLayout(orientation='vertical', size_hint_y=0.2, spacing=dp(5))
        input_layout.add_widget(Label(text='請輸入姓名:', size_hint_y=0.3))
        self.name_input = TextInput(multiline=False, size_hint_y=0.7)
        input_layout.add_widget(self.name_input)
        layout.add_widget(input_layout)
        
        # 分析按鈕
        analyze_btn = Button(text='開始分析', size_hint_y=0.1)
        analyze_btn.bind(on_press=self.analyze)
        layout.add_widget(analyze_btn)
        
        # 結果區
        self.result_scroll = ScrollView(size_hint_y=0.6)
        self.result_label = Label(text='輸入姓名後點擊分析...', markup=True, size_hint_y=None)
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_scroll.add_widget(self.result_label)
        layout.add_widget(self.result_scroll)
        
        self.add_widget(layout)
    
    def analyze(self, instance):
        name = self.name_input.text.strip()
        if name:
            try:
                # 使用 analyze_jiugong 方法（需要名字、年、月、日）
                # 如果沒有出生日期，使用預設值
                result = self.analyzer.analyze_jiugong(name, 1990, 1, 1)
                self.result_label.text = f'[b]九宮分析結果 - {name}[/b]\n\n{result}'
            except Exception as e:
                self.result_label.text = f'[b]分析錯誤[/b]\n\n{str(e)}'
        else:
            self.result_label.text = '[color=ff0000]請輸入有效的姓名[/color]'


class AstrologyScreen(Screen):
    """星座分析螢幕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzer = ZodiacSignAnalyzer()
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # 標題
        title = Label(text='[b]星座分析[/b]', size_hint_y=0.08, markup=True, font_size='24sp')
        layout.add_widget(title)
        
        # 輸入區
        input_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=0.25)
        
        input_layout.add_widget(Label(text='姓名:', size_hint_y=None, height=dp(30)))
        self.name_input = TextInput(multiline=False, size_hint_y=None, height=dp(40))
        input_layout.add_widget(self.name_input)
        
        input_layout.add_widget(Label(text='出生日期 (YYYY-MM-DD):', size_hint_y=None, height=dp(30)))
        self.date_input = TextInput(text='1990-01-01', multiline=False, size_hint_y=None, height=dp(40))
        input_layout.add_widget(self.date_input)
        
        input_layout.add_widget(Label(text='血型:', size_hint_y=None, height=dp(30)))
        self.blood_spinner = Spinner(
            text='O型',
            values=('A型', 'B型', 'AB型', 'O型'),
            size_hint_y=None,
            height=dp(40)
        )
        input_layout.add_widget(self.blood_spinner)
        
        layout.add_widget(input_layout)
        
        # 分析按鈕
        analyze_btn = Button(text='開始分析', size_hint_y=0.08)
        analyze_btn.bind(on_press=self.analyze)
        layout.add_widget(analyze_btn)
        
        # 結果區
        self.result_scroll = ScrollView(size_hint_y=0.59)
        self.result_label = Label(text='輸入資訊後點擊分析...', markup=True, size_hint_y=None)
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_scroll.add_widget(self.result_label)
        layout.add_widget(self.result_scroll)
        
        self.add_widget(layout)
    
    def analyze(self, instance):
        name = self.name_input.text.strip()
        date = self.date_input.text.strip()
        blood = self.blood_spinner.text
        
        if name and date:
            try:
                # 解析日期（格式: YYYY-MM-DD）
                parts = date.split('-')
                if len(parts) == 3:
                    month = int(parts[1])
                    day = int(parts[2])
                    result = self.analyzer.analyze_zodiac(month, day)
                    blood_info = f'\n血型: {blood}' if blood else ''
                    self.result_label.text = f'[b]星座分析結果 - {name}[/b]{blood_info}\n\n{result}'
                else:
                    self.result_label.text = '[color=ff0000]日期格式錯誤，請使用 YYYY-MM-DD[/color]'
            except Exception as e:
                self.result_label.text = f'[b]分析錯誤[/b]\n\n{str(e)}'
        else:
            self.result_label.text = '[color=ff0000]請輸入完整資訊[/color]'


class BaziScreen(Screen):
    """八字分析螢幕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.analyzer = BaziAnalyzer()
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # 標題
        title = Label(text='[b]八字分析[/b]', size_hint_y=0.08, markup=True, font_size='24sp')
        layout.add_widget(title)
        
        # 輸入區
        input_layout = GridLayout(cols=1, spacing=dp(5), size_hint_y=0.28)
        
        inputs = [
            ('年:', 'year_input', '1990'),
            ('月:', 'month_input', '1'),
            ('日:', 'day_input', '1'),
            ('時:', 'hour_input', '12'),
        ]
        
        for label_text, input_name, default in inputs:
            input_layout.add_widget(Label(text=label_text, size_hint_y=None, height=dp(25)))
            inp = TextInput(text=default, multiline=False, size_hint_y=None, height=dp(35))
            setattr(self, input_name, inp)
            input_layout.add_widget(inp)
        
        layout.add_widget(input_layout)
        
        # 分析按鈕
        analyze_btn = Button(text='開始分析', size_hint_y=0.08)
        analyze_btn.bind(on_press=self.analyze)
        layout.add_widget(analyze_btn)
        
        # 結果區
        self.result_scroll = ScrollView(size_hint_y=0.56)
        self.result_label = Label(text='輸入出生時間後點擊分析...', markup=True, size_hint_y=None)
        self.result_label.bind(texture_size=self.result_label.setter('size'))
        self.result_scroll.add_widget(self.result_label)
        layout.add_widget(self.result_scroll)
        
        self.add_widget(layout)
    
    def analyze(self, instance):
        try:
            year = int(self.year_input.text)
            month = int(self.month_input.text)
            day = int(self.day_input.text)
            hour = int(self.hour_input.text)
            
            result = self.analyzer.analyze_bazi(year, month, day, hour)
            # 結果可能是字典或字符串
            if isinstance(result, dict):
                result_text = '\n'.join([f'{k}: {v}' for k, v in result.items()])
            else:
                result_text = str(result)
            self.result_label.text = f'[b]八字分析結果[/b]\n{year}年{month}月{day}日 {hour}時\n\n{result_text}'
        except Exception as e:
            self.result_label.text = f'[b]分析錯誤[/b]\n\n{str(e)}'


class MainScreen(Screen):
    """主螢幕"""
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.build_ui()
    
    def build_ui(self):
        layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
        
        # 標題
        title_label = Label(
            text='[b]Jeff命理世界[/b]\n命理分析系統 v6.7',
            size_hint_y=0.15,
            markup=True,
            font_size='28sp'
        )
        layout.add_widget(title_label)
        
        # 功能按鈕區（使用 ScrollView 支持更多功能）
        scroll = ScrollView(size_hint_y=0.85)
        button_layout = GridLayout(cols=2, spacing=dp(10), size_hint_y=None)
        button_layout.bind(minimum_height=button_layout.setter('height'))
        
        # 功能按鈕
        features = [
            ('九宮分析', 'jiugong'),
            ('星座分析', 'astrology'),
            ('八字分析', 'bazi'),
            ('紫微分析', 'purplestar'),
            ('塔羅牌', 'tarot'),
            ('周易卜卦', 'yijing'),
            ('血型分析', 'blood'),
            ('名字分析', 'name'),
        ]
        
        for feature_name, screen_name in features:
            btn = Button(
                text=feature_name,
                size_hint_y=None,
                height=dp(80),
                font_size='16sp'
            )
            btn.bind(on_press=partial(self.go_to_screen, screen_name))
            button_layout.add_widget(btn)
        
        scroll.add_widget(button_layout)
        layout.add_widget(scroll)
        
        self.add_widget(layout)
    
    def go_to_screen(self, screen_name, instance):
        self.manager.current = screen_name


class JeffMingliApp(App):
    """主應用程式類"""
    
    def build(self):
        """建立應用介面"""
        self.title = 'Jeff命理世界 - Android版'
        
        # 建立螢幕管理器
        sm = ScreenManager()
        
        # 添加主螢幕
        main_screen = MainScreen(name='main')
        sm.add_widget(main_screen)
        
        # 添加功能螢幕
        jiugong_screen = JiuGongScreen(name='jiugong')
        sm.add_widget(jiugong_screen)
        
        astrology_screen = AstrologyScreen(name='astrology')
        sm.add_widget(astrology_screen)
        
        bazi_screen = BaziScreen(name='bazi')
        sm.add_widget(bazi_screen)
        
        # 其他螢幕的佔位符
        for screen_name in ['purplestar', 'tarot', 'yijing', 'blood', 'name']:
            placeholder_screen = Screen(name=screen_name)
            placeholder_layout = BoxLayout(orientation='vertical', spacing=dp(10), padding=dp(10))
            placeholder_layout.add_widget(Label(text=f'[b]{screen_name.upper()} - 開發中[/b]', markup=True, font_size='24sp'))
            back_btn = Button(text='返回主菜單', size_hint_y=0.1)
            back_btn.bind(on_press=lambda x: setattr(sm, 'current', 'main'))
            placeholder_layout.add_widget(back_btn)
            placeholder_screen.add_widget(placeholder_layout)
            sm.add_widget(placeholder_screen)
        
        return sm


if __name__ == '__main__':
    app = JeffMingliApp()
    app.run()
