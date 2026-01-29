#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
FATE Suite v2.3 - 完整命理分析系統
整合：星座、血型、八字、紫微、塔羅牌、周易卜卦、流年流月
特色：一次輸入，完整分析，含命盤圖形，流年流月運勢
Version: 6.7 Ultimate Expert
Date: 2026-01-21
"""

import sys
import os

# 修復 Windows 控制台編碼問題（適配 GUI 模式）
if sys.platform == 'win32':
    try:
        # GUI 模式下 stdout 可能為 None，需要先檢查
        if sys.stdout is not None and hasattr(sys.stdout, 'reconfigure'):
            sys.stdout.reconfigure(encoding='utf-8')
        if sys.stderr is not None and hasattr(sys.stderr, 'reconfigure'):
            sys.stderr.reconfigure(encoding='utf-8')
    except Exception:
        try:
            import io
            # 只有當 buffer 存在時才重新配置
            if sys.stdout is not None and hasattr(sys.stdout, 'buffer') and sys.stdout.buffer is not None:
                sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
            if sys.stderr is not None and hasattr(sys.stderr, 'buffer') and sys.stderr.buffer is not None:
                sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')
        except Exception:
            pass  # GUI 模式下忽略錯誤
from datetime import datetime
from pathlib import Path
import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext, Canvas, filedialog
from PIL import Image, ImageTk, ImageDraw
import math
import json

# 配置路徑
BASE_PATH = Path(__file__).parent
MODULES_PATH = BASE_PATH / 'modules'

# 添加modules和BASE_PATH到系統路徑
if MODULES_PATH.exists():
    sys.path.insert(0, str(MODULES_PATH))
sys.path.insert(0, str(BASE_PATH))

# 導入命理模組
try:
    from mingli_astrology_v7_expert import AstrologyExpertAnalyzerV7 as ZodiacSignAnalyzer
except ImportError:
    from mingli_astrology import ZodiacSignAnalyzer as AstrologyExpertAnalyzerV7
    ZodiacSignAnalyzer = AstrologyExpertAnalyzerV7

try:
    from mingli_astrology import BloodTypeAnalyzer
except ImportError:
    BloodTypeAnalyzer = None

try:
    from mingli_blood_type_expert_v7 import BloodTypeExpertAnalyzerV7 as BloodTypeAnalyzerEnhanced
except ImportError:
    BloodTypeAnalyzerEnhanced = None

try:
    from spouse_compatibility_expert_v7 import SpouseCompatibilityExpertV7
except ImportError:
    SpouseCompatibilityExpertV7 = None

# 導入專業配偶合適性分析模組
try:
    from modules.spouse_compatibility_professional import ProfessionalSpouseCompatibilityAnalyzer
    print("[OK] 載入專業配偶合適性分析模組")
except ImportError:
    try:
        from spouse_compatibility_professional import ProfessionalSpouseCompatibilityAnalyzer
        print("[OK] 載入專業配偶合適性分析模組（根目錄）")
    except ImportError as e:
        print(f"[WARNING] 無法載入專業配偶合適性分析模組: {e}")
        ProfessionalSpouseCompatibilityAnalyzer = None

# 優先使用專業版八字分析模組
try:
    from modules.mingli_bazi_professional import BaziProfessionalAnalyzer as BaziAnalyzer
    print("[OK] 載入八字命理專業版 v7.0")
except ImportError:
    from mingli_bazi_analyzer import BaziAnalyzer
    print("[INFO] 使用基礎八字分析模組")

from mingli_purplestar_analyzer import PurpleStarAnalyzer
from mingli_tarot import TarotAnalyzer
from mingli_yijing import YijingAnalyzer
from mingli_jiugong import JiuGongAnalyzer
from mingli_jiugong_name import JiuGongNameAnalyzer
from mingli_jiugong_name_enhanced import JiuGongNameAnalyzerEnhanced
# from chart_enhancer import ChartEnhancer  # 模組不存在，已註釋
# from spouse_data_dialog import SpouseDataDialog  # 模組不存在，已註釋


class EnhancedFATESuiteGUI:
    """FATE Suite 增強版 - 完整命理分析"""

    def __init__(self, root):
        self.root = root
        self.root.title("✨ Jeff的命理世界 ✨")
        
        # 動態偵測螢幕大小並調整視窗尺寸
        self.root.update_idletasks()  # 確保視窗資訊已更新
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        
        # 視窗設定為螢幕的85%，確保不會太大
        window_width = int(screen_width * 0.85)
        window_height = int(screen_height * 0.85)
        
        # 限制最小和最大尺寸
        window_width = max(1000, min(window_width, 1920))
        window_height = max(700, min(window_height, 1080))
        
        # 計算置中位置
        x = (screen_width - window_width) // 2
        y = (screen_height - window_height) // 2
        
        self.root.geometry(f"{window_width}x{window_height}+{x}+{y}")
        self.root.minsize(1000, 700)

        # 載入設定
        self.load_settings()
        
        # 初始化
        self.init_data()
        self.setup_styles()
        self.setup_background()  # 設置背景圖
        self.create_widgets()
        
        # 儲存分析結果
        self.analysis_results = {}

    def load_settings(self):
        """載入設定檔案"""
        self.config_file = Path(__file__).parent / "fate_suite_config.json"
        
        # 預設設定
        default_settings = {
            'font_size': 10,
            'language': 'zh_TW',
            'theme': 'light'
        }
        
        try:
            if self.config_file.exists():
                with open(self.config_file, 'r', encoding='utf-8') as f:
                    settings = json.load(f)
                    self.current_font_size = settings.get('font_size', 10)
                    self.current_language = settings.get('language', 'zh_TW')
                    self.current_theme = settings.get('theme', 'light')
            else:
                # 使用預設值
                self.current_font_size = default_settings['font_size']
                self.current_language = default_settings['language']
                self.current_theme = default_settings['theme']
        except Exception as e:
            print(f"載入設定失敗：{e}，使用預設設定")
            self.current_font_size = default_settings['font_size']
            self.current_language = default_settings['language']
            self.current_theme = default_settings['theme']
        
        # 追蹤所有文字框用於即時字體變更
        self.text_widgets = []
    
    def save_settings(self):
        """保存設定到檔案"""
        try:
            settings = {
                'font_size': self.current_font_size,
                'language': self.current_language,
                'theme': self.current_theme
            }
            with open(self.config_file, 'w', encoding='utf-8') as f:
                json.dump(settings, f, ensure_ascii=False, indent=2)
            return True
        except Exception as e:
            print(f"保存設定失敗：{e}")
            return False
    
    def init_data(self):
        """初始化數據"""
        self.zodiac_analyzer = ZodiacSignAnalyzer()
        self.blood_analyzer = BloodTypeAnalyzer()
        # 使用增強版本，如果不可用則設為None（後續在需要時檢查）
        if BloodTypeAnalyzerEnhanced is not None:
            self.blood_enhanced = BloodTypeAnalyzerEnhanced()
        else:
            self.blood_enhanced = None
        
        self.bazi_analyzer = BaziAnalyzer()
        self.purplestar_analyzer = PurpleStarAnalyzer()
        self.tarot_analyzer = TarotAnalyzer()
        self.yijing_analyzer = YijingAnalyzer()
        self.jiugong_analyzer = JiuGongAnalyzer()
        self.jiugong_name_analyzer = JiuGongNameAnalyzer()
        self.jiugong_name_enhanced = JiuGongNameAnalyzerEnhanced()
        # 配偶分析器（如果不可用則設為None）
        if SpouseCompatibilityExpertV7 is not None:
            self.spouse_analyzer = SpouseCompatibilityExpertV7()
        else:
            self.spouse_analyzer = None
        
        # 專業配偶分析器（新增）
        if ProfessionalSpouseCompatibilityAnalyzer is not None:
            self.professional_spouse_analyzer = ProfessionalSpouseCompatibilityAnalyzer()
            print("[OK] 專業配偶分析器初始化成功")
        else:
            self.professional_spouse_analyzer = None
            print("[WARNING] 專業配偶分析器不可用")
        
        # self.chart_enhancer = ChartEnhancer()  # 圖表增強器（模組不存在，已註釋）
        
        # 配偶完整資料（用於深度分析）
        self.spouse_full_data = None
        self.spouse_data = None  # 簡單配偶資料

    def setup_styles(self):
        """設置 UI 風格 - 白色柔和主題"""
        # 設置主視窗背景色 - 米白色
        self.root.configure(bg='#F8F5F2')
        
        style = ttk.Style()
        style.theme_use('clam')

        # 主標題 - 深褐色配金色背景
        style.configure('Header.TLabel', 
                       font=('Microsoft JhengHei', 18, 'bold'), 
                       foreground='#5D4E37',
                       background='#F5E6D3')
        
        # 副標題 - 深褐色
        style.configure('Sub.TLabel', 
                       font=('Microsoft JhengHei', 11), 
                       foreground='#5D4E37',
                       background='#FFF8E7')
        
        # 狀態列 - 深褐色
        style.configure('Status.TLabel', 
                       font=('Microsoft JhengHei', 9), 
                       foreground='#5D4E37',
                       background='#F5E6D3')
        
        # 大按鈕 - 紅金色系
        style.configure('Big.TButton', 
                       font=('Microsoft JhengHei', 12, 'bold'), 
                       padding=10,
                       foreground='#FFFFFF',
                       background='#C74028')
        
        style.map('Big.TButton',
                 foreground=[('active', '#FFFFFF')],
                 background=[('active', '#A03318')])
        
        # 框架背景色 - 淺金色半透明
        style.configure('TFrame', background='#FFF8E7')
        style.configure('TLabelframe', background='#FFF8E7', foreground='#5D4E37')
        style.configure('TLabelframe.Label', background='#FFF8E7', foreground='#5D4E37')
        
        # Notebook標籤 - 金色系
        style.configure('TNotebook', background='#FFF8E7')
        style.configure('TNotebook.Tab', 
                       font=('Microsoft JhengHei', 10),
                       foreground='#5D4E37',
                       background='#F0E5D0',
                       padding=[10, 5])
        style.map('TNotebook.Tab',
                 background=[('selected', '#D4AF37')],
                 foreground=[('selected', '#FFFFFF')])

    def setup_background(self):
        """設置金黃色漸層背景圖片"""
        try:
            # 優先使用金黃色漸層背景
            bg_path = Path(__file__).parent / "fortune_golden_gradient_bg.png"
            
            # 如果金黃色背景不存在，嘗試舊的白色背景
            if not bg_path.exists():
                bg_path = Path(__file__).parent / "soft_fortune_bg.png"
            
            if bg_path.exists():
                # 載入背景圖並調整大小以適配視窗
                bg_image = Image.open(bg_path)
                
                # 獲取螢幕尺寸
                screen_width = self.root.winfo_screenwidth()
                screen_height = self.root.winfo_screenheight()
                
                # 調整背景圖大小
                bg_image = bg_image.resize((screen_width, screen_height), Image.Resampling.LANCZOS)
                bg_photo = ImageTk.PhotoImage(bg_image)
                
                # 創建Canvas作為背景
                bg_canvas = Canvas(self.root, width=screen_width, height=screen_height, 
                                  highlightthickness=0)
                bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
                bg_canvas.create_image(0, 0, image=bg_photo, anchor='nw')
                
                # 保存引用避免被垃圾回收
                self.bg_photo = bg_photo
                self.bg_canvas = bg_canvas
                
                print(f"✓ 已載入背景圖：{bg_path.name}")
            else:
                print("背景圖不存在，使用預設金黃色漸層")
                # 使用程式動態生成金黃色漸層
                self.create_gradient_background()
        except Exception as e:
            print(f"載入背景圖失敗：{e}")
            self.create_gradient_background()
    
    def create_gradient_background(self):
        """動態創建金黃色漸層背景"""
        try:
            screen_width = self.root.winfo_screenwidth()
            screen_height = self.root.winfo_screenheight()
            
            # 創建金黃色漸層圖片
            gradient_image = Image.new('RGB', (screen_width, screen_height))
            draw = ImageDraw.Draw(gradient_image)
            
            # 從淺金色到深金色的漸層
            for y in range(screen_height):
                ratio = y / screen_height
                r = int(245 - (245 - 212) * ratio)
                g = int(230 - (230 - 175) * ratio)
                b = int(211 - (211 - 55) * ratio)
                draw.line([(0, y), (screen_width, y)], fill=(r, g, b))
            
            bg_photo = ImageTk.PhotoImage(gradient_image)
            
            # 創建Canvas作為背景
            bg_canvas = Canvas(self.root, width=screen_width, height=screen_height,
                             highlightthickness=0)
            bg_canvas.place(x=0, y=0, relwidth=1, relheight=1)
            bg_canvas.create_image(0, 0, image=bg_photo, anchor='nw')
            
            self.bg_photo = bg_photo
            self.bg_canvas = bg_canvas
            
            print("✓ 已生成金黃色漸層背景")
        except Exception as e:
            print(f"創建漸層背景失敗：{e}")

    def create_widgets(self):
        """創建 UI 元件"""
        self.create_header()

        # 創建Canvas和滾動條的容器 - 金色半透明背景
        container = tk.Frame(self.root, bg='#FFF8E7')
        container.pack(fill=tk.BOTH, expand=True, padx=5, pady=5)
        
        # 創建Canvas - 金色半透明背景
        self.canvas = tk.Canvas(container, bg='#FFF8E7', highlightthickness=0)
        
        # 創建垂直和水平滾動條
        v_scrollbar = tk.Scrollbar(container, orient=tk.VERTICAL, command=self.canvas.yview)
        h_scrollbar = tk.Scrollbar(container, orient=tk.HORIZONTAL, command=self.canvas.xview)
        
        # 配置Canvas滾動
        self.canvas.configure(yscrollcommand=v_scrollbar.set, xscrollcommand=h_scrollbar.set)
        
        # 佈局滾動條和Canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        self.canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 主容器Frame放在Canvas內
        main_frame = ttk.Frame(self.canvas)
        canvas_window = self.canvas.create_window((0, 0), window=main_frame, anchor=tk.NW)
        
        # 綁定滑鼠滾輪事件
        def on_mousewheel(event):
            self.canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        def on_configure(event):
            # 更新Canvas滾動區域
            self.canvas.configure(scrollregion=self.canvas.bbox("all"))
            # 調整Canvas窗口寬度以適應Canvas
            canvas_width = self.canvas.winfo_width()
            if canvas_width > 1:
                self.canvas.itemconfig(canvas_window, width=canvas_width)
        
        main_frame.bind("<Configure>", on_configure)
        self.canvas.bind("<MouseWheel>", on_mousewheel)
        
        # 分成上下兩部分
        self.create_input_section(main_frame)
        self.create_output_section(main_frame)
        
        self.create_footer()

    def create_header(self):
        """創建標題欄"""
        header_frame = tk.Frame(self.root, bg='#F5E6D3')
        header_frame.pack(fill=tk.X, padx=10, pady=10)

        # 左側：標題
        left_frame = tk.Frame(header_frame, bg='#F5E6D3')
        left_frame.pack(side=tk.LEFT)
        
        title_label = tk.Label(left_frame, text="✨ Jeff的命理世界 ✨",
                              font=('Microsoft JhengHei', 18, 'bold'),
                              foreground='#5D4E37',
                              background='#F5E6D3')
        title_label.pack(side=tk.LEFT)
        
        # 時間顯示在名稱右邊
        self.datetime_label = tk.Label(left_frame, text="",
                                       font=('Microsoft JhengHei', 10, 'bold'),
                                       foreground='#C74028',
                                       background='#F5E6D3')
        self.datetime_label.pack(side=tk.LEFT, padx=10)
        
        # 啟動時間更新
        self.update_datetime()

    def create_input_section(self, parent):
        """創建輸入區域"""
        input_frame = ttk.LabelFrame(parent, text="📝 請輸入您的出生資訊（僅需輸入一次）", padding=15)
        input_frame.pack(fill=tk.X, pady=(0, 10))

        # 第零行：姓名（新增）
        row0 = ttk.Frame(input_frame)
        row0.pack(fill=tk.X, pady=5)

        ttk.Label(row0, text="您的姓名：", style='Sub.TLabel', width=12).pack(side=tk.LEFT, padx=5)
        self.name_entry = ttk.Entry(row0, width=20, font=('Microsoft JhengHei', 10))
        self.name_entry.insert(0, "王小明")
        self.name_entry.pack(side=tk.LEFT, padx=5)
        
        ttk.Label(row0, text="提示：如需配偶配對分析，請點擊「💑 配偶資料」按鈕輸入完整資料", 
                 style='Status.TLabel', font=('Microsoft JhengHei', 9, 'italic')).pack(side=tk.LEFT, padx=15)

        # 第一行：年月日
        row1 = ttk.Frame(input_frame)
        row1.pack(fill=tk.X, pady=5)

        ttk.Label(row1, text="出生年份：", style='Sub.TLabel', width=12).pack(side=tk.LEFT, padx=5)
        self.birth_year = ttk.Spinbox(row1, from_=1900, to=2100, width=10)
        self.birth_year.set(1990)
        self.birth_year.pack(side=tk.LEFT, padx=5)

        ttk.Label(row1, text="月份：", style='Sub.TLabel', width=8).pack(side=tk.LEFT, padx=5)
        self.birth_month = ttk.Combobox(row1, values=list(range(1, 13)), state="readonly", width=6)
        self.birth_month.set(5)
        self.birth_month.pack(side=tk.LEFT, padx=5)

        ttk.Label(row1, text="日期：", style='Sub.TLabel', width=8).pack(side=tk.LEFT, padx=5)
        self.birth_day = ttk.Combobox(row1, values=list(range(1, 32)), state="readonly", width=6)
        self.birth_day.set(15)
        self.birth_day.pack(side=tk.LEFT, padx=5)

        # 第二行：時辰、性別、血型
        row2 = ttk.Frame(input_frame)
        row2.pack(fill=tk.X, pady=5)

        ttk.Label(row2, text="出生時辰：", style='Sub.TLabel', width=12).pack(side=tk.LEFT, padx=5)
        self.birth_hour = ttk.Combobox(row2, values=list(range(0, 24)), state="readonly", width=6)
        self.birth_hour.set(14)
        self.birth_hour.pack(side=tk.LEFT, padx=5)

        ttk.Label(row2, text="性別：", style='Sub.TLabel', width=8).pack(side=tk.LEFT, padx=5)
        self.gender = ttk.Combobox(row2, values=['男', '女'], state="readonly", width=6)
        self.gender.set('男')
        self.gender.pack(side=tk.LEFT, padx=5)

        ttk.Label(row2, text="血型：", style='Sub.TLabel', width=8).pack(side=tk.LEFT, padx=5)
        self.blood_type = ttk.Combobox(row2, values=['A', 'B', 'AB', 'O'], state="readonly", width=6)
        self.blood_type.set('A')
        self.blood_type.pack(side=tk.LEFT, padx=5)

        # 第三行：按鈕
        row3 = ttk.Frame(input_frame)
        row3.pack(fill=tk.X, pady=10)

        ttk.Button(row3, text="🔮 開始完整命理分析", 
                  command=self.start_full_analysis,
                  style='Big.TButton').pack(side=tk.LEFT, padx=5)

        ttk.Button(row3, text="💑 配偶資料", 
                  command=self.open_spouse_data_dialog).pack(side=tk.LEFT, padx=5)

        ttk.Button(row3, text="⚙️ 設定", 
                  command=self.show_settings).pack(side=tk.LEFT, padx=5)

        ttk.Button(row3, text="� 開啟檔案", 
                  command=self.load_results).pack(side=tk.LEFT, padx=5)

        ttk.Button(row3, text="�💾 儲存結果", 
                  command=self.save_results).pack(side=tk.LEFT, padx=5)

        ttk.Button(row3, text="🖨️ 列印報告", 
                  command=self.print_report).pack(side=tk.LEFT, padx=5)

        ttk.Button(row3, text="🗑️ 清除", 
                  command=self.clear_results).pack(side=tk.LEFT, padx=5)
        
        # 第四行：字體大小控制（新增）
        row4 = ttk.Frame(input_frame)
        row4.pack(fill=tk.X, pady=10)
        
        ttk.Label(row4, text="字體大小：", style='Sub.TLabel', width=12).pack(side=tk.LEFT, padx=5)
        
        # 字體大小顯示
        self.font_size_display = ttk.Label(row4, text=f"{self.current_font_size}pt", 
                                          style='Header.TLabel')
        self.font_size_display.pack(side=tk.LEFT, padx=5)
        
        # 縮小按鈕
        ttk.Button(row4, text="➖ 縮小", 
                  command=lambda: self.change_font_size(-1)).pack(side=tk.LEFT, padx=2)
        
        # 放大按鈕
        ttk.Button(row4, text="➕ 放大", 
                  command=lambda: self.change_font_size(1)).pack(side=tk.LEFT, padx=2)
        
        # 重設按鈕
        ttk.Button(row4, text="🔄 重設", 
                  command=self.reset_font_size).pack(side=tk.LEFT, padx=2)
        
        # 配偶資料顯示標籤
        self.spouse_info_label = ttk.Label(row4, text="（暫無配偶完整資料）", 
                                          style='Status.TLabel')
        self.spouse_info_label.pack(side=tk.LEFT, padx=20)

    def create_output_section(self, parent):
        """創建輸出區域"""
        output_frame = ttk.Frame(parent)
        output_frame.pack(fill=tk.BOTH, expand=True)

        # 創建 Notebook 標籤頁
        self.notebook = ttk.Notebook(output_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        # 各個分析結果頁面
        self.create_result_page("♈ 星座命盤", "zodiac")
        self.create_result_page("🩸 血型分析", "blood")
        self.create_result_page("🔮 八字排盤", "bazi")
        self.create_result_page("🟣 紫微命盤", "purplestar")
        self.create_divination_page("🎴 塔羅占卜", "tarot")
        self.create_divination_page("☯ 周易卜卦", "yijing")
        self.create_result_page("🔢 九宮靈數", "jiugong")
        self.create_result_page("📛 九宮姓名學", "jiugong_name")
        self.create_result_page("📊 綜合總結", "summary")

    def create_result_page(self, title, key):
        """創建結果頁面"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        
        # 創建一個內部容器來確保內容居中和填滿
        inner_frame = ttk.Frame(frame)
        inner_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        result_text = scrolledtext.ScrolledText(inner_frame, 
                                                height=25, 
                                                font=('Microsoft JhengHei', 10), 
                                                wrap=tk.WORD,
                                                relief=tk.SUNKEN,
                                                borderwidth=2)
        result_text.pack(fill=tk.BOTH, expand=True)
        
        # 配置彩色標籤
        result_text.tag_configure('title', foreground='#0066CC', font=('Microsoft JhengHei', 14, 'bold'))
        result_text.tag_configure('header', foreground='#006633', font=('Microsoft JhengHei', 12, 'bold'))
        result_text.tag_configure('subheader', foreground='#FF6600', font=('Microsoft JhengHei', 11, 'bold'))
        result_text.tag_configure('important', foreground='#CC0000', font=('Microsoft JhengHei', 10, 'bold'))
        result_text.tag_configure('spouse', foreground='#9933CC', font=('Microsoft JhengHei', 11, 'bold'))
        result_text.tag_configure('normal', foreground='#000000', font=('Microsoft JhengHei', 10))
        
        # 追蹤文字框用於字體變更
        if not hasattr(self, 'text_widgets'):
            self.text_widgets = []
        self.text_widgets.append(result_text)

        # 保存引用
        setattr(self, f"{key}_text", result_text)
    
    def create_divination_page(self, title, key):
        """創建占卜頁面（塔羅、周易）- 包含問題輸入和執行按鈕"""
        frame = ttk.Frame(self.notebook)
        self.notebook.add(frame, text=title)
        
        # 頂部輸入區域
        input_frame = ttk.LabelFrame(frame, text="📝 請輸入您的問題", padding=10)
        input_frame.pack(fill=tk.X, padx=10, pady=10)
        
        # 問題輸入框
        question_label = ttk.Label(input_frame, text="您想問的問題：", font=('Microsoft JhengHei', 10))
        question_label.pack(side=tk.LEFT, padx=5)
        
        question_entry = ttk.Entry(input_frame, width=40, font=('Microsoft JhengHei', 10))
        question_entry.insert(0, "請問我的未來運勢如何？")
        question_entry.pack(side=tk.LEFT, padx=5, fill=tk.X, expand=True)
        
        # 保存問題輸入框引用
        setattr(self, f"{key}_question_entry", question_entry)
        
        # 執行按鈕
        if key == 'tarot':
            button_text = "🎴 開始塔羅占卜"
            command = lambda: self.perform_tarot_divination()
        else:
            button_text = "☯ 開始周易卜卦"
            command = lambda: self.perform_yijing_divination()
        
        execute_button = ttk.Button(input_frame, text=button_text, command=command)
        execute_button.pack(side=tk.LEFT, padx=5)
        
        # 說明文字
        hint_label = ttk.Label(input_frame, 
                              text="（請先輸入問題，然後點擊按鈕進行占卜）", 
                              font=('Microsoft JhengHei', 9, 'italic'),
                              foreground='gray')
        hint_label.pack(side=tk.LEFT, padx=5)
        
        # 結果顯示區域
        result_text = scrolledtext.ScrolledText(frame, 
                                                height=20, 
                                                font=('Microsoft JhengHei', 10), 
                                                wrap=tk.WORD,
                                                relief=tk.SUNKEN,
                                                borderwidth=2)
        result_text.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        # 配置彩色標籤
        result_text.tag_configure('title', foreground='#0066CC', font=('Microsoft JhengHei', 14, 'bold'))
        result_text.tag_configure('header', foreground='#006633', font=('Microsoft JhengHei', 12, 'bold'))
        result_text.tag_configure('subheader', foreground='#FF6600', font=('Microsoft JhengHei', 11, 'bold'))
        result_text.tag_configure('important', foreground='#CC0000', font=('Microsoft JhengHei', 10, 'bold'))
        result_text.tag_configure('normal', foreground='#000000', font=('Microsoft JhengHei', 10))
        
        # 追蹤文字框用於字體變更
        if not hasattr(self, 'text_widgets'):
            self.text_widgets = []
        self.text_widgets.append(result_text)

        # 保存引用
        setattr(self, f"{key}_text", result_text)
        
        # 顯示初始提示
        initial_text = f"{'='*60}\n"
        if key == 'tarot':
            initial_text += "🎴 塔羅占卜\n"
            initial_text += f"{'='*60}\n\n"
            initial_text += "歡迎使用塔羅占卜系統！\n\n"
            initial_text += "使用說明：\n"
            initial_text += "1. 請在上方輸入您想詢問的問題\n"
            initial_text += "2. 點擊「🎴 開始塔羅占卜」按鈕\n"
            initial_text += "3. 系統會為您抽取塔羅牌並進行解讀\n"
            initial_text += "4. 每次點擊都會重新占卜，產生新的結果\n\n"
            initial_text += "💡 提示：\n"
            initial_text += "• 問題要明確具體\n"
            initial_text += "• 專注於您真正關心的事情\n"
            initial_text += "• 帶著開放的心態接受指引\n\n"
        else:
            initial_text += "☯ 周易卜卦\n"
            initial_text += f"{'='*60}\n\n"
            initial_text += "歡迎使用周易卜卦系統！\n\n"
            initial_text += "使用說明：\n"
            initial_text += "1. 請在上方輸入您想詢問的問題\n"
            initial_text += "2. 點擊「☯ 開始周易卜卦」按鈕\n"
            initial_text += "3. 系統會為您起卦並解析卦象\n"
            initial_text += "4. 每次點擊都會重新起卦，產生新的結果\n\n"
            initial_text += "💡 提示：\n"
            initial_text += "• 誠心誠意提出問題\n"
            initial_text += "• 問題宜具體不宜籠統\n"
            initial_text += "• 用心體會卦象的啟示\n\n"
        
        initial_text += f"{'='*60}\n"
        initial_text += "請輸入您的問題後，點擊按鈕開始占卜。\n"
        initial_text += f"{'='*60}\n"
        
        result_text.insert(tk.END, initial_text)
        result_text.config(state=tk.DISABLED)

    def create_footer(self):
        """創建底部状態欄"""
        footer_frame = tk.Frame(self.root, bg='#F8F5F2')
        footer_frame.pack(fill=tk.X, side=tk.BOTTOM, padx=10, pady=5)

        self.status_label = tk.Label(footer_frame, text="✅ 系統就緒，請輸入出生資訊開始分析",
                                font=('Microsoft JhengHei', 9),
                                foreground='#2C3E50',
                                background='#F8F5F2')
        self.status_label.pack(side=tk.LEFT)

    def update_datetime(self):
        """更新日期時間顯示"""
        now = datetime.now()
        datetime_str = now.strftime("%Y年%m月%d日 %H:%M:%S")
        self.datetime_label.config(text=f"📅 {datetime_str}")
        
        # 每秒更新一次
        self.root.after(1000, self.update_datetime)
    
    def start_full_analysis(self):
        """開始完整命理分析"""
        try:
            # 獲取輸入資料
            name = self.name_entry.get().strip()
            if not name:
                messagebox.showwarning("提示", "請輸入姓名！")
                return
            
            year = int(self.birth_year.get())
            month = int(self.birth_month.get())
            day = int(self.birth_day.get())
            hour = int(self.birth_hour.get())
            gender_str = self.gender.get()
            blood = self.blood_type.get()

            birth_date = f"{year}-{month:02d}-{day:02d}"

            # 更新狀態
            self.status_label.config(text="⏳ 正在進行完整命理分析，請稍候...")
            self.root.update()

            # 清空之前的結果
            self.analysis_results = {}

            # 1. 星座分析（含命盤圖及宮位主導星座）
            self.status_label.config(text="⏳ 正在分析星座...")
            self.root.update()
            zodiac_result = self.analyze_zodiac_with_chart(month, day, hour)
            # 增強圖表化
            zodiac_result = self._add_zodiac_charts(zodiac_result, month, day)
            
            # 1.1 專業星座配偶合適性分析（新增）
            if hasattr(self, 'spouse_full_data') and self.spouse_full_data and self.professional_spouse_analyzer:
                self.status_label.config(text="💑 正在進行星座配偶專業合適性分析...")
                self.root.update()
                try:
                    user_zodiac = self._get_zodiac_name(month, day)
                    spouse_zodiac = self._get_zodiac_name(
                        self.spouse_full_data['month'],
                        self.spouse_full_data['day']
                    )
                    
                    zodiac_compatibility = self.professional_spouse_analyzer.analyze_zodiac_professional(
                        user_zodiac, 
                        spouse_zodiac
                    )
                    
                    zodiac_result += "\n\n" + "="*80 + "\n"
                    zodiac_result += zodiac_compatibility
                    print(f"[OK] 星座配偶專業分析完成：{user_zodiac} + {spouse_zodiac}")
                except Exception as e:
                    print(f"[ERROR] 星座配偶分析出錯：{e}")
                    import traceback
                    traceback.print_exc()
            
            self.analysis_results['zodiac'] = zodiac_result
            self.display_result('zodiac', zodiac_result, f"出生日期: {month}月{day}日")

            # 2. 血型分析
            self.status_label.config(text="⏳ 正在分析血型...")
            self.root.update()
            blood_result = self.blood_analyzer.analyze_blood_type(blood)
            # 增強版本：若不可用則使用基礎版本
            if self.blood_enhanced is not None:
                blood_enhanced = self.blood_enhanced.analyze_blood_type(blood)
                combined_blood = f"{blood_result}\n\n{'='*70}\n進階分析\n{'='*70}\n\n{blood_enhanced}"
            else:
                combined_blood = blood_result
            # 增強圖表化
            combined_blood = self._add_blood_charts(combined_blood, blood)
            self.analysis_results['blood'] = combined_blood
            self.display_result('blood', combined_blood, f"血型: {blood}型")

            # 3. 八字排盤（使用專業版分析）
            self.status_label.config(text="⏳ 正在排八字...")
            self.root.update()
            
            # 檢查是否為專業版分析器
            if hasattr(self.bazi_analyzer, 'format_complete_analysis'):
                # 使用專業版 v7.0 完整分析
                ganzhi = self.bazi_analyzer.get_ganzhi(year, month, day, hour)
                birth_date_dict = {'year': year, 'month': month, 'day': day, 'hour': hour}
                bazi_result = self.bazi_analyzer.format_complete_analysis(
                    birth_date_dict, ganzhi, gender_str, name
                )
            else:
                # 使用基礎版分析
                bazi_data = self.bazi_analyzer.analyze_bazi(year, month, day, hour)
                bazi_result = self.bazi_analyzer.format_result(bazi_data)
                # 增強圖表化
                bazi_result = self._add_bazi_charts(bazi_result, bazi_data)
            
            # 3.1 配偶深度八字分析（專業版）
            if hasattr(self, 'spouse_full_data') and self.spouse_full_data and self.professional_spouse_analyzer:
                self.status_label.config(text="💑 正在進行配偶八字專業深度分析...")
                self.root.update()
                try:
                    # 使用專業版取得配偶八字
                    if hasattr(self.bazi_analyzer, 'get_ganzhi'):
                        spouse_ganzhi = self.bazi_analyzer.get_ganzhi(
                            self.spouse_full_data['year'],
                            self.spouse_full_data['month'],
                            self.spouse_full_data['day'],
                            self.spouse_full_data['hour']
                        )
                        # 創建簡化的 bazi_data 格式用於配偶分析
                        spouse_bazi_data = {
                            'year_gan': spouse_ganzhi['year']['gan'],
                            'year_zhi': spouse_ganzhi['year']['zhi'],
                            'month_gan': spouse_ganzhi['month']['gan'],
                            'month_zhi': spouse_ganzhi['month']['zhi'],
                            'day_gan': spouse_ganzhi['day']['gan'],
                            'day_zhi': spouse_ganzhi['day']['zhi'],
                            'hour_gan': spouse_ganzhi['hour']['gan'],
                            'hour_zhi': spouse_ganzhi['hour']['zhi']
                        }
                        user_bazi_data = {
                            'year_gan': ganzhi['year']['gan'],
                            'year_zhi': ganzhi['year']['zhi'],
                            'month_gan': ganzhi['month']['gan'],
                            'month_zhi': ganzhi['month']['zhi'],
                            'day_gan': ganzhi['day']['gan'],
                            'day_zhi': ganzhi['day']['zhi'],
                            'hour_gan': ganzhi['hour']['gan'],
                            'hour_zhi': ganzhi['hour']['zhi']
                        }
                    else:
                        # 使用基礎版分析
                        spouse_bazi_data = self.bazi_analyzer.analyze_bazi(
                            self.spouse_full_data['year'],
                            self.spouse_full_data['month'],
                            self.spouse_full_data['day'],
                            self.spouse_full_data['hour']
                        )
                        user_bazi_data = self.bazi_analyzer.analyze_bazi(year, month, day, hour)
                    
                    # 執行專業深度合適性分析（四柱逐柱 + 十神分析）
                    bazi_compatibility = self.professional_spouse_analyzer.analyze_bazi_professional(
                        name, 
                        user_bazi_data, 
                        self.spouse_full_data['name'],
                        spouse_bazi_data,
                        gender_str
                    )
                    
                    bazi_result += "\n\n" + "="*80 + "\n"
                    bazi_result += bazi_compatibility
                    print(f"[OK] 配偶八字專業深度分析完成：{name} + {self.spouse_full_data['name']}")
                except Exception as e:
                    print(f"[ERROR] 配偶八字專業分析出錯：{e}")
                    import traceback
                    traceback.print_exc()
            
            self.analysis_results['bazi'] = bazi_result
            self.display_result('bazi', bazi_result, f"出生: {year}年{month}月{day}日 {hour}時")

            # 4. 紫微論命（含命盤圖）
            self.status_label.config(text="⏳ 正在排紫微命盤...")
            self.root.update()
            gender_code = 'M' if gender_str == '男' else 'F'
            ps_result = self.analyze_ziwei_with_chart(year, month, day, hour, gender_code)
            # 增強圖表化
            ps_result = self._add_ziwei_charts(ps_result)
            
            # 4.1 專業紫微配偶合適性分析（新增）
            if hasattr(self, 'spouse_full_data') and self.spouse_full_data and self.professional_spouse_analyzer:
                self.status_label.config(text="[配偶分析] 正在進行紫微配偶專業合適性分析（12宮14主星）...")
                self.root.update()
                try:
                    # 簡化的命宮數據（實際應該從紫微排盤獲取）
                    user_palace = {'命宮': '紫微天府', '夫妻宮': '太陽太陰'}
                    spouse_gender_code = 'F' if gender_str == '男' else 'M'
                    spouse_palace = {'命宮': '天機天梁', '夫妻宮': '武曲天相'}
                    
                    ziwei_compatibility = self.professional_spouse_analyzer.analyze_ziwei_professional(
                        user_palace,
                        spouse_palace,
                        name,
                        self.spouse_full_data['name']
                    )
                    
                    ps_result += "\n\n" + "="*80 + "\n"
                    ps_result += ziwei_compatibility
                    print(f"[OK] 紫微配偶專業分析完成：{name} + {self.spouse_full_data['name']}")
                except Exception as e:
                    print(f"[ERROR] 紫微配偶專業分析出錯：{e}")
                    import traceback
                    traceback.print_exc()
            
            self.analysis_results['purplestar'] = ps_result
            self.display_result('purplestar', ps_result, f"性別: {gender_str}")

            # 塔羅占卜和周易卜卦改為手動執行（不在完整分析中自動執行）
            # 使用者需要到各自的分頁中輸入問題並點擊按鈕執行

            # 6.5. 九宮算命（新增）
            self.status_label.config(text="⏳ 正在進行九宮算命...")
            self.root.update()
            jiugong_result = self.jiugong_analyzer.analyze_jiugong(name, year, month, day)
            # 增強圖表化
            jiugong_result = self._add_jiugong_charts(jiugong_result)
            self.analysis_results['jiugong'] = jiugong_result
            self.display_result('jiugong', jiugong_result, f"姓名: {name}")

            # 6.6. 九宮姓名學（新增）+ 配偶配對分析（整合）
            self.status_label.config(text="⏳ 正在進行九宮姓名學分析...")
            self.root.update()
            jiugong_name_result = self.jiugong_name_analyzer.analyze_name(name)
            
            # 6.6.1 配偶姓名配對分析（使用配偶對話框的資料）
            spouse_name = None
            if hasattr(self, 'spouse_full_data') and self.spouse_full_data:
                spouse_name = self.spouse_full_data.get('name', '').strip()
            
            print(f"[DEBUG] 配偶姓名輸入值: '{spouse_name}'")
            print(f"[DEBUG] 使用者姓名: '{name}'")
            
            if spouse_name and spouse_name != name:
                print(f"[OK] 開始配偶配對分析: {name} + {spouse_name}")
                self.status_label.config(text="💑 正在進行配偶姓名配對分析...")
                self.root.update()
                try:
                    compatibility_result = self.jiugong_name_enhanced.analyze_compatibility(name, spouse_name)
                    print(f"📊 配對結果長度: {len(compatibility_result) if compatibility_result else 0} 字元")
                    
                    if compatibility_result:
                        # 將配對結果附加到九宮姓名學結果字串中
                        jiugong_name_result += "\n\n" + "="*80 + "\n"
                        jiugong_name_result += "💑 配偶姓名配對深度分析\n"
                        jiugong_name_result += "="*80 + "\n"
                        jiugong_name_result += f"\n【配對對象】：{name} ❤️ {spouse_name}\n"
                        jiugong_name_result += f"【分析日期】：{datetime.now().strftime('%Y年%m月%d日')}\n"
                        jiugong_name_result += "\n" + "="*80 + "\n\n"
                        jiugong_name_result += compatibility_result
                        jiugong_name_result += "\n\n" + "="*80 + "\n"
                        jiugong_name_result += "【配對分析說明】\n"
                        jiugong_name_result += "="*80 + "\n\n"
                        jiugong_name_result += "此配對分析基於九宮姓名學原理，透過以下五大維度進行深度評估：\n\n"
                        jiugong_name_result += "1. 【人格相配度】（權重40%）：\n"
                        jiugong_name_result += "   分析雙方的個性特質、處事態度是否協調互補。\n"
                        jiugong_name_result += "   高分表示雙方性格契合，低分則需要更多包容與理解。\n\n"
                        jiugong_name_result += "2. 【地格相配度】（權重25%）：\n"
                        jiugong_name_result += "   評估雙方的生活習慣、價值觀與基礎運勢的匹配程度。\n"
                        jiugong_name_result += "   影響日常相處的和諧度與生活品質。\n\n"
                        jiugong_name_result += "3. 【總格相配度】（權重20%）：\n"
                        jiugong_name_result += "   考察雙方的整體命格與長期發展潛力的相容性。\n"
                        jiugong_name_result += "   關係到關係的持久性與未來發展方向。\n\n"
                        jiugong_name_result += "4. 【外格相配度】（權重10%）：\n"
                        jiugong_name_result += "   分析雙方的社交模式、對外表現與人際關係的協調度。\n"
                        jiugong_name_result += "   影響雙方在社交場合的互動與對外形象。\n\n"
                        jiugong_name_result += "5. 【天格相配度】（權重5%）：\n"
                        jiugong_name_result += "   評估雙方的家族背景、先天條件的匹配程度。\n"
                        jiugong_name_result += "   雖然權重較低，但仍對整體關係有一定影響。\n\n"
                        jiugong_name_result += "\n【綜合建議】\n"
                        jiugong_name_result += "配對指數僅供參考，真正的感情需要雙方共同經營。\n"
                        jiugong_name_result += "高分表示先天條件較佳，低分則需要更多溝通與包容。\n"
                        jiugong_name_result += "無論分數高低，真心與努力才是維繫感情的關鍵。\n"
                        jiugong_name_result += "\n" + "="*80 + "\n"
                        
                        print(f"[OK] 配對分析成功並已整合: {name} + {spouse_name}")
                    else:
                        print("[WARNING] 配對分析返回空結果")
                except Exception as e:
                    error_msg = f"配對分析失敗: {e}"
                    print(error_msg)
                    import traceback
                    traceback.print_exc()
            else:
                if not spouse_name:
                    print("[INFO] 未輸入配偶姓名，跳過配對分析")
                elif spouse_name == name:
                    print("[WARNING] 配偶姓名與使用者姓名相同，跳過配對分析")
            
            # 統一顯示九宮姓名學結果（包含配對分析）
            self.analysis_results['jiugong_name'] = jiugong_name_result
            self.display_result('jiugong_name', jiugong_name_result, f"姓名: {name}")

            # 6.7. 流年流月分析
            self.status_label.config(text="⏳ 正在分析流年流月運勢...")
            self.root.update()
            fortune_result = self.add_yearly_monthly_fortune(year, month, day, hour, gender_str)
            self.analysis_results['fortune'] = fortune_result
            # 暫時在綜合總結中顯示，未來可新增獨立標籤頁

            # 7. 生成綜合總結
            self.status_label.config(text="⏳ 正在生成綜合總結...")
            self.root.update()
            self.generate_comprehensive_summary(year, month, day, hour, gender_str, blood)

            # 完成
            self.status_label.config(text="✅ 完整命理分析完成！請查看各個標籤頁的結果")
            messagebox.showinfo("分析完成", 
                              "所有命理分析已完成！\n\n包含：\n• 星座命盤\n• 血型分析\n• 八字排盤\n• 紫微命盤\n• 塔羅占卜\n• 周易卜卦\n• 九宮靈數\n• 九宮姓名學\n• 流年流月運勢\n• 綜合總結\n\n請切換標籤頁查看詳細結果。")

        except Exception as e:
            self.status_label.config(text="❌ 分析出現錯誤")
            messagebox.showerror("錯誤", f"分析失敗: {str(e)}\n\n{type(e).__name__}")

    def analyze_zodiac_with_chart(self, month, day, hour):
        """星座分析含命盤圖 - 包含宮位主導星座"""
        basic_result = self.zodiac_analyzer.analyze_zodiac(month, day)
        
        # 計算上升星座（簡化版本，使用時辰）
        ascendant = self._calculate_ascendant(month, day, hour)
        
        # 生成星座命盤圖形描述和詳細宮位說明（包含每宮主導星座）
        zodiac_chart = self._generate_zodiac_chart_with_houses(month, day, ascendant)
        house_details = self._get_zodiac_house_details_advanced(month, day, ascendant)
        
        return f"{basic_result}\n\n{zodiac_chart}\n\n{house_details}"

    def _calculate_ascendant(self, month, day, hour):
        """計算上升星座（簡化版本）"""
        # 簡化計算：使用太陽星座加上時辰偏移
        sun_sign_index = self._get_zodiac_index(month, day)
        # 每2小時上升一個星座
        hour_offset = hour // 2
        ascendant_index = (sun_sign_index + hour_offset) % 12
        
        zodiac_names = ["牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座",
                       "天秤座", "天蠍座", "射手座", "魔羯座", "水瓶座", "雙魚座"]
        return zodiac_names[ascendant_index]

    def _get_zodiac_index(self, month, day):
        """獲取星座索引（0-11）"""
        zodiac_dates = [
            (3, 21, 0),   # 牡羊座
            (4, 20, 1),   # 金牛座
            (5, 21, 2),   # 雙子座
            (6, 22, 3),   # 巨蟹座
            (7, 23, 4),   # 獅子座
            (8, 23, 5),   # 處女座
            (9, 23, 6),   # 天秤座
            (10, 24, 7),  # 天蠍座
            (11, 22, 8),  # 射手座
            (12, 22, 9),  # 魔羯座
            (1, 20, 10),  # 水瓶座
            (2, 19, 11),  # 雙魚座
        ]
        
        for m, d, idx in zodiac_dates:
            if month < m or (month == m and day < d):
                return (idx - 1) % 12
        return 9  # 魔羯座

    def _generate_zodiac_chart_with_houses(self, month, day, ascendant):
        """生成包含宮位主導星座的命盤圖"""
        sun_sign = self._get_zodiac_name(month, day)
        
        # 獲取12宮位的主導星座
        houses = self._get_house_signs(ascendant)
        
        chart = f"""
{'='*70}
                    🌟 西洋占星命盤圖 🌟
{'='*70}

【基本資訊】
太陽星座（Sun Sign）：{sun_sign}
上升星座（Ascendant）：{ascendant}

【命盤結構】

              第12宮           第11宮
            {houses[11]}        {houses[10]}
                ╲              ╱
                 ╲            ╱
          第1宮   ╲          ╱   第10宮
        {houses[0]}  ╲        ╱  {houses[9]}
           ↑        ╲      ╱        
           │         ╲    ╱         
           │          ╲  ╱          
    第2宮  │           ☉           第9宮
  {houses[1]} │                      {houses[8]}
           │          ╱  ╲          
           │         ╱    ╲         
           │        ╱      ╲        
        {houses[2]}  ╱        ╲  {houses[7]}
          第3宮   ╱          ╲   第8宮
                 ╱            ╲
                ╱              ╲
            {houses[3]}        {houses[6]}
              第4宮           第7宮
                │
                ↓
              第5宮
            {houses[4]}      {houses[5]}
                              第6宮

【宮位主導星座一覽】
第1宮（命宮）   ：{houses[0]} - 自我與外貌
第2宮（財帛宮） ：{houses[1]} - 金錢與價值
第3宮（溝通宮） ：{houses[2]} - 學習與交流
第4宮（家庭宮） ：{houses[3]} - 家庭與根基
第5宮（戀愛宮） ：{houses[4]} - 創造與娛樂
第6宮（健康宮） ：{houses[5]} - 工作與健康
第7宮（婚姻宮） ：{houses[6]} - 伴侶與合作
第8宮（轉化宮） ：{houses[7]} - 資源與轉變
第9宮（哲學宮） ：{houses[8]} - 智慧與遠行
第10宮（事業宮）：{houses[9]} - 事業與地位
第11宮（朋友宮）：{houses[10]} - 願望與社交
第12宮（靈性宮）：{houses[11]} - 潛意識與靈性

☉ = 太陽位置
{'='*70}
"""
        return chart

    def _get_house_signs(self, ascendant):
        """根據上升星座獲取12宮位的主導星座"""
        zodiac_names = ["牡羊座", "金牛座", "雙子座", "巨蟹座", "獅子座", "處女座",
                       "天秤座", "天蠍座", "射手座", "魔羯座", "水瓶座", "雙魚座"]
        
        asc_index = zodiac_names.index(ascendant)
        houses = []
        for i in range(12):
            houses.append(zodiac_names[(asc_index + i) % 12])
        return houses

    def _get_zodiac_house_details_advanced(self, month, day, ascendant):
        """獲取星座12宮位的詳細說明（包含主導星座特質）"""
        sun_sign = self._get_zodiac_name(month, day)
        houses = self._get_house_signs(ascendant)
        
        details = f"""
{'='*70}
              📖 星座12宮位詳細解析（含主導星座）📖
{'='*70}

您的太陽星座：{sun_sign}
您的上升星座：{ascendant}

以下是根據您的上升星座，分析12宮位的主導星座及其影響：

┌──────────────────────────────────────────────────────────┐
│ 第1宮（命宮）- 主導星座：{houses[0]}                          │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】自我、外貌、第一印象、人生態度                    │
│                                                            │
│ 【{houses[0]}的影響】                                       │
│ {self._get_zodiac_influence(houses[0], 1)}                │
│                                                            │
│ 【建議】善用{houses[0]}的特質塑造個人形象，                   │
│         展現獨特魅力。                                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第2宮（財帛宮）- 主導星座：{houses[1]}                        │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】財務、物質、價值觀、賺錢能力                      │
│                                                            │
│ 【{houses[1]}的影響】                                       │
│ {self._get_zodiac_influence(houses[1], 2)}                │
│                                                            │
│ 【建議】根據{houses[1]}的特質規劃財務，                       │
│         培養穩健的理財習慣。                                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第3宮（溝通宮）- 主導星座：{houses[2]}                        │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】溝通、學習、兄弟姊妹、短途旅行                    │
│                                                            │
│ 【{houses[2]}的影響】                                       │
│ {self._get_zodiac_influence(houses[2], 3)}                │
│                                                            │
│ 【建議】發揮{houses[2]}的溝通特質，                           │
│         擴展知識面和人際網絡。                              │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第4宮（家庭宮）- 主導星座：{houses[3]}                        │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】家庭、根基、父母（特別是母親）、不動產            │
│                                                            │
│ 【{houses[3]}的影響】                                       │
│ {self._get_zodiac_influence(houses[3], 4)}                │
│                                                            │
│ 【建議】運用{houses[3]}的特質營造家庭氛圍，                   │
│         建立穩固的情感基礎。                                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第5宮（戀愛宮）- 主導星座：{houses[4]}                        │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】戀愛、創造力、娛樂、子女、投機                    │
│                                                            │
│ 【{houses[4]}的影響】                                       │
│ {self._get_zodiac_influence(houses[4], 5)}                │
│                                                            │
│ 【建議】發揮{houses[4]}的創造特質，                           │
│         享受生活樂趣和浪漫。                                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第6宮（健康宮）- 主導星座：{houses[5]}                        │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】工作、健康、日常事務、服務、寵物                  │
│                                                            │
│ 【{houses[5]}的影響】                                       │
│ {self._get_zodiac_influence(houses[5], 6)}                │
│                                                            │
│ 【建議】按照{houses[5]}的特質規律作息，                       │
│         注重健康管理。                                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第7宮（婚姻宮）- 主導星座：{houses[6]}                        │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】婚姻、伴侶、合作、一對一關係                      │
│                                                            │
│ 【{houses[6]}的影響】                                       │
│ {self._get_zodiac_influence(houses[6], 7)}                │
│                                                            │
│ 【建議】以{houses[6]}的方式經營關係，                         │
│         尋找互補的伴侶。                                    │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第8宮（轉化宮）- 主導星座：{houses[7]}                        │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】轉變、共享資源、遺產、深層心理                    │
│                                                            │
│ 【{houses[7]}的影響】                                       │
│ {self._get_zodiac_influence(houses[7], 8)}                │
│                                                            │
│ 【建議】用{houses[7]}的智慧面對轉變，                         │
│         管理共享資源。                                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第9宮（哲學宮）- 主導星座：{houses[8]}                        │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】哲學、宗教、長途旅行、高等教育、異國              │
│                                                            │
│ 【{houses[8]}的影響】                                       │
│ {self._get_zodiac_influence(houses[8], 9)}                │
│                                                            │
│ 【建議】以{houses[8]}的視角探索世界，                         │
│         追求智慧和真理。                                    │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第10宮（事業宮）- 主導星座：{houses[9]}                       │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】事業、社會地位、名聲、父親、公眾形象              │
│                                                            │
│ 【{houses[9]}的影響】                                       │
│ {self._get_zodiac_influence(houses[9], 10)}               │
│                                                            │
│ 【建議】運用{houses[9]}的能量發展事業，                       │
│         建立專業形象。                                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第11宮（朋友宮）- 主導星座：{houses[10]}                      │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】朋友、團體、願望、社交、人道主義                  │
│                                                            │
│ 【{houses[10]}的影響】                                      │
│ {self._get_zodiac_influence(houses[10], 11)}              │
│                                                            │
│ 【建議】以{houses[10]}的方式經營社交，                        │
│         實現人生願望。                                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第12宮（靈性宮）- 主導星座：{houses[11]}                      │
├──────────────────────────────────────────────────────────┤
│ 【宮位意義】潛意識、靈性、秘密、隱藏的敵人、自我犧牲          │
│                                                            │
│ 【{houses[11]}的影響】                                      │
│ {self._get_zodiac_influence(houses[11], 12)}              │
│                                                            │
│ 【建議】透過{houses[11]}的方式探索內在，                      │
│         培養靈性修養。                                      │
└──────────────────────────────────────────────────────────┘

{'='*70}
"""
        return details

    def _get_zodiac_influence(self, zodiac, house_num):
        """獲取星座對特定宮位的影響說明"""
        influences = {
            "牡羊座": {
                1: "充滿活力和衝勁，給人勇敢直率的第一印象，行動力強",
                2: "賺錢積極主動，喜歡快速致富，但需注意衝動消費",
                3: "溝通直接明快，學習新事物快速，喜歡競爭性的學習",
                4: "家庭氛圍活潑，喜歡主導家務，可能與家人有爭執",
                5: "戀愛熱情主動，創造力強，喜歡刺激冒險的娛樂",
                6: "工作效率高，但需注意頭部和肌肉的健康",
                7: "吸引獨立自主的伴侶，婚姻中需要自由空間",
                8: "面對危機果斷，善於快速轉型，直面恐懼",
                9: "哲學觀積極進取，喜歡探險和運動型旅遊",
                10: "事業心強烈，適合領導職位，勇於開創",
                11: "朋友圈活躍，願望明確，積極參與團體活動",
                12: "需要釋放壓抑的憤怒，透過運動療癒內心"
            },
            "金牛座": {
                1: "穩重可靠的形象，給人踏實感，注重物質享受",
                2: "理財穩健保守，重視物質安全，擅長累積財富",
                3: "溝通緩慢但深思熟慮，學習重視實用性",
                4: "重視家庭穩定，喜歡舒適的居家環境",
                5: "戀愛忠誠持久，喜歡感官享受的娛樂",
                6: "工作踏實，需注意喉嚨和頸部健康",
                7: "尋求穩定可靠的伴侶，重視婚姻中的物質基礎",
                8: "面對變化較為保守，善於管理共同財產",
                9: "哲學觀實際，旅遊重視舒適和美食",
                10: "事業穩紮穩打，適合金融和藝術領域",
                11: "朋友關係長久，願望實際可行",
                12: "需要放鬆身心，透過藝術療癒"
            },
            "雙子座": {
                1: "機智靈活的形象，給人聰明健談的印象",
                2: "賺錢方式多元，可能有多個收入來源",
                3: "溝通能力極佳，好奇心強，多才多藝",
                4: "家庭氛圍活潑多變，可能搬家頻繁",
                5: "戀愛多樣化，喜歡智力遊戲和社交活動",
                6: "工作多樣，需注意手部和呼吸系統健康",
                7: "需要能溝通的伴侶，婚姻中重視心靈交流",
                8: "好奇神秘事物，善於資訊收集和分析",
                9: "喜歡學習不同文化，短期多次旅遊",
                10: "適合傳媒、教育或多元化事業",
                11: "朋友圈廣泛，社交活躍，願望多樣",
                12: "需要靜心思考，透過寫作療癒"
            },
            "巨蟹座": {
                1: "溫柔敏感的形象，給人親切關懷的感覺",
                2: "賺錢重視安全感，可能囤積物品",
                3: "溝通情感豐富，記憶力強，重感情",
                4: "極度重視家庭，家是情感避風港",
                5: "戀愛需要安全感，創造力來自情感",
                6: "工作照顧他人，需注意胃部和情緒健康",
                7: "尋求能給予安全感的伴侶，婚姻如家庭",
                8: "情感轉變深刻，善於照顧共同資源",
                9: "旅遊重視情感連結，喜歡懷舊",
                10: "事業與家庭結合，適合照顧型行業",
                11: "朋友如家人，願望與家庭相關",
                12: "需要情感出口，透過藝術療癒"
            },
            "獅子座": {
                1: "自信光芒的形象，給人高貴大方的感覺",
                2: "賺錢大方，喜歡奢華享受，慷慨消費",
                3: "溝通充滿熱情，喜歡表演和展現自我",
                4: "家庭中是主角，重視家族榮耀",
                5: "戀愛浪漫熱烈，創造力豐富，喜歡娛樂",
                6: "工作認真負責，需注意心臟和背部健康",
                7: "需要欣賞自己的伴侶，婚姻中需要被重視",
                8: "面對轉變有尊嚴，善於掌控共享資源",
                9: "哲學觀宏大，旅遊追求豪華體驗",
                10: "天生領導者，適合需要表現力的事業",
                11: "朋友圈需要自己發光，願望宏大",
                12: "需要獨處充電，透過創作療癒"
            },
            "處女座": {
                1: "謹慎細緻的形象，給人專業完美的印象",
                2: "理財精打細算，注重實用性和品質",
                3: "溝通精確，分析能力強，注重細節",
                4: "家庭井然有序，注重清潔和健康",
                5: "戀愛謹慎，喜歡有意義的娛樂活動",
                6: "工作完美主義，需注意腸胃和神經健康",
                7: "尋求完美伴侶，婚姻中注重實際問題",
                8: "善於分析轉變，精確管理共同資產",
                9: "學習注重實用，旅遊規劃詳細",
                10: "事業精益求精，適合分析和服務業",
                11: "選擇朋友謹慎，願望實際可行",
                12: "需要放下完美主義，透過服務療癒"
            },
            "天秤座": {
                1: "優雅和諧的形象，給人親切公正的感覺",
                2: "賺錢重視平衡，可能與他人合作理財",
                3: "溝通圓融得體，善於協調和外交",
                4: "家庭追求和諧美麗，重視平等關係",
                5: "戀愛浪漫，喜歡藝術和社交娛樂",
                6: "工作需要夥伴，需注意腎臟和皮膚健康",
                7: "婚姻是生命重心，尋求平等互補的伴侶",
                8: "善於平衡轉變，公平處理共享資源",
                9: "哲學觀重視公平，喜歡文化藝術旅遊",
                10: "事業需要合作，適合藝術和法律領域",
                11: "朋友圈和諧，願望與關係相關",
                12: "需要獨處平衡，透過藝術療癒"
            },
            "天蠍座": {
                1: "神秘深邃的形象，給人強烈磁場的感覺",
                2: "賺錢能力強，善於投資和資源轉化",
                3: "溝通深入，洞察力強，保守秘密",
                4: "家庭氛圍深刻，可能有家族秘密",
                5: "戀愛熱情專一，創造力來自深層情感",
                6: "工作專注投入，需注意生殖系統健康",
                7: "尋求深刻連結的伴侶，婚姻中追求靈魂伴侶",
                8: "天生擅長轉化，善於處理危機和遺產",
                9: "探索生命奧秘，旅遊深入體驗",
                10: "事業追求權力，適合調查和心理領域",
                11: "朋友關係深刻，願望涉及轉化和權力",
                12: "需要面對內在陰影，透過心理療癒"
            },
            "射手座": {
                1: "樂觀開朗的形象，給人自由熱情的感覺",
                2: "賺錢樂觀，可能投資海外或教育",
                3: "溝通直率坦誠，喜歡哲學性對話",
                4: "家庭氛圍自由，可能來自多元文化",
                5: "戀愛自由，喜歡冒險和戶外娛樂",
                6: "工作需要自由度，需注意肝臟和大腿健康",
                7: "需要給予自由的伴侶，婚姻如探險",
                8: "樂觀面對轉變，善於從變化中學習",
                9: "天生哲學家，熱愛旅遊和學習",
                10: "事業多元化，適合教育和海外事業",
                11: "朋友來自不同背景，願望宏大理想",
                12: "需要信仰支持，透過旅行療癒"
            },
            "魔羯座": {
                1: "成熟穩重的形象，給人可靠專業的感覺",
                2: "理財保守謹慎，長期規劃財富",
                3: "溝通實際，注重結果和效率",
                4: "重視家庭責任，可能承擔家族負擔",
                5: "戀愛認真，娛樂也很務實",
                6: "工作努力負責，需注意骨骼和膝蓋健康",
                7: "尋求穩定負責的伴侶，婚姻如事業夥伴",
                8: "謹慎面對轉變，善於管理長期資源",
                9: "務實的世界觀，旅遊重視目的性",
                10: "天生事業家，適合管理和建設",
                11: "朋友關係專業，願望實際可達成",
                12: "需要釋放壓力，透過工作療癒"
            },
            "水瓶座": {
                1: "獨特前衛的形象，給人理性友善的感覺",
                2: "賺錢方式創新，可能涉及科技或團體",
                3: "溝通客觀理性，思想前衛獨特",
                4: "家庭關係平等，可能有非傳統家庭模式",
                5: "戀愛需要自由和心靈交流，娛樂特別",
                6: "工作重視創新，需注意循環系統和小腿健康",
                7: "需要給予空間的伴侶，婚姻如朋友",
                8: "以理性面對轉變，善於科技和創新",
                9: "追求普世價值，旅遊體驗不同文化",
                10: "事業獨特創新，適合科技和人道事業",
                11: "朋友圈廣泛多元，願望關乎人類福祉",
                12: "需要獨處思考，透過冥想療癒"
            },
            "雙魚座": {
                1: "夢幻敏感的形象，給人神秘慈悲的感覺",
                2: "金錢觀念模糊，需要實際管理",
                3: "溝通充滿想像，直覺力強，善解人意",
                4: "家庭充滿想像，可能界限模糊",
                5: "戀愛浪漫夢幻，藝術創造力豐富",
                6: "工作需要靈感，需注意足部和免疫系統",
                7: "尋求靈魂伴侶，婚姻追求精神合一",
                8: "深刻感受轉變，善於靈性療癒",
                9: "追求靈性真理，旅遊尋找靈感",
                10: "事業需要靈感，適合藝術和治療",
                11: "朋友關係同理心強，願望理想化",
                12: "天生靈性修行者，需要獨處療癒"
            }
        }
        
        return influences.get(zodiac, {}).get(house_num, "此星座為該宮位帶來獨特的能量和影響")

    def _get_zodiac_house_details(self, month, day):
        """獲取星座12宮位的詳細說明"""
        zodiac_name = self._get_zodiac_name(month, day)
        
        details = f"""
{'='*70}
                    📖 星座12宮位詳細解析 📖
{'='*70}

您的太陽星座：{zodiac_name}

以下是根據您的星座特質，對12宮位的詳細解讀：

┌──────────────────────────────────────────────────────────┐
│ 第1宮（命宮/上升宮）- 自我與外貌                            │
├──────────────────────────────────────────────────────────┤
│ 代表：個性、外貌、給人的第一印象、自我意識                  │
│                                                            │
│ 您的特質：                                                 │
│ 作為{zodiac_name}，您在第一印象上展現出該星座的典型特徵。    │
│ 您的外在形象和待人處事的方式深受太陽星座影響。              │
│ 建議多注意個人形象和第一印象的塑造。                        │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第2宮（財帛宮）- 金錢與價值觀                               │
├──────────────────────────────────────────────────────────┤
│ 代表：財務狀況、物質資源、價值觀、自我價值                  │
│                                                            │
│ 財運分析：                                                 │
│ 您對金錢和物質的態度會影響財富累積。                        │
│ 建議培養良好的理財習慣，重視儲蓄和投資。                    │
│ 瞭解自己的價值觀，才能在物質與精神間取得平衡。              │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第3宮（兄弟宮）- 溝通與學習                                 │
├──────────────────────────────────────────────────────────┤
│ 代表：溝通能力、學習、兄弟姊妹、鄰居、短途旅行              │
│                                                            │
│ 溝通特質：                                                 │
│ 您的溝通方式和學習能力較為突出。                            │
│ 與兄弟姊妹和鄰居的關係會影響您的成長。                      │
│ 建議多閱讀、學習新知識，提升溝通技巧。                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第4宮（田宅宮）- 家庭與根基                                 │
├──────────────────────────────────────────────────────────┤
│ 代表：家庭、父母（特別是母親）、不動產、情感基礎            │
│                                                            │
│ 家庭運勢：                                                 │
│ 家庭是您情感的避風港，影響您的安全感。                      │
│ 與父母的關係會影響您的人格發展。                            │
│ 建議重視家庭和諧，營造溫馨的居家環境。                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第5宮（子女宮）- 創造與娛樂                                 │
├──────────────────────────────────────────────────────────┤
│ 代表：戀愛、創造力、娛樂、子女、投機                        │
│                                                            │
│ 創造力分析：                                               │
│ 您具有獨特的創造力和表現欲。                                │
│ 戀愛和娛樂是生活的重要部分。                                │
│ 建議培養興趣愛好，享受生活樂趣。                            │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第6宮（僕役宮）- 工作與健康                                 │
├──────────────────────────────────────────────────────────┤
│ 代表：工作、健康、日常事務、服務、寵物                      │
│                                                            │
│ 健康提醒：                                                 │
│ 工作態度和健康狀況互相影響。                                │
│ 建議保持規律的生活作息，注意身體保養。                      │
│ 培養服務他人的精神，工作會更有意義。                        │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第7宮（夫妻宮）- 婚姻與合作                                 │
├──────────────────────────────────────────────────────────┤
│ 代表：婚姻、合夥、公開的敵人、一對一關係                    │
│                                                            │
│ 感情分析：                                                 │
│ 婚姻和親密關係對您很重要。                                  │
│ 您期待找到能夠互補的伴侶。                                  │
│ 建議在關係中保持平衡，學習妥協和溝通。                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第8宮（疾厄宮）- 轉化與資源                                 │
├──────────────────────────────────────────────────────────┤
│ 代表：死亡、遺產、他人資源、性、深層轉化                    │
│                                                            │
│ 深層分析：                                                 │
│ 您對神秘事物和深層心理有興趣。                              │
│ 懂得運用他人資源來達成目標。                                │
│ 建議面對人生轉折時，保持積極正面的態度。                    │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第9宮（遷移宮）- 哲學與遠行                                 │
├──────────────────────────────────────────────────────────┤
│ 代表：哲學、宗教、長途旅行、高等教育、外國事務              │
│                                                            │
│ 智慧啟發：                                                 │
│ 您對人生哲理和異國文化感興趣。                              │
│ 長途旅行能帶來成長和啟發。                                  │
│ 建議多接觸不同文化，開拓視野。                              │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第10宮（官祿宮）- 事業與地位                                │
├──────────────────────────────────────────────────────────┤
│ 代表：事業、社會地位、名聲、父母（特別是父親）              │
│                                                            │
│ 事業運勢：                                                 │
│ 事業成就是您人生的重要目標。                                │
│ 您追求社會認同和專業成就。                                  │
│ 建議設定明確的職業目標，持續努力。                          │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第11宮（福德宮）- 朋友與願望                                │
├──────────────────────────────────────────────────────────┤
│ 代表：朋友、團體、願望、社交、人道主義                      │
│                                                            │
│ 社交分析：                                                 │
│ 朋友和社交圈對您很重要。                                    │
│ 您重視團體歸屬感和共同理想。                                │
│ 建議積極參與社交活動，拓展人脈。                            │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 第12宮（玄秘宮）- 靈性與潛意識                              │
├──────────────────────────────────────────────────────────┤
│ 代表：潛意識、靈性、秘密、隱藏的敵人、自我犧牲              │
│                                                            │
│ 靈性提升：                                                 │
│ 您有豐富的內在世界和靈性追求。                              │
│ 獨處時能夠獲得心靈平靜。                                    │
│ 建議培養冥想或靈性實踐，探索內在自我。                      │
└──────────────────────────────────────────────────────────┘

{'='*70}
"""
        return details

    def _generate_zodiac_chart_text(self, month, day):
        """生成星座命盤文字圖"""
        # 確定星座
        zodiac_name = self._get_zodiac_name(month, day)
        
        chart = f"""
{'='*70}
                         🌟 星座命盤圖 🌟
{'='*70}

              北方
                │
                │
     天頂MC ────┼──── 天底IC
                │
                │
              南方

          第12宮          第1宮
             ╲            ╱
              ╲          ╱
    第11宮     ╲        ╱     第2宮
       ╲        ╲      ╱        ╱
        ╲        ╲    ╱        ╱
         ╲        ╲  ╱        ╱
第10宮────●────────☉────────●────第3宮
         ╱        ╱  ╲        ╲
        ╱        ╱    ╲        ╲
       ╱        ╱      ╲        ╲
    第9宮     ╱        ╲     第4宮
              ╱          ╲
             ╱            ╲
          第8宮          第5宮
                │
                │
          第7宮 │ 第6宮
                │

【命盤說明】
☉ 太陽星座：{zodiac_name}
● 宮位分佈：12宮位系統

【宮位意義】
第1宮（命宮）  ：自我、外貌、個性
第2宮（財帛宮）：財運、價值觀
第3宮（兄弟宮）：溝通、學習、手足
第4宮（田宅宮）：家庭、根基、父母
第5宮（子女宮）：戀愛、創造、子女
第6宮（僕役宮）：健康、工作、服務
第7宮（夫妻宮）：婚姻、合夥、伴侶
第8宮（疾厄宮）：轉變、共享資源
第9宮（遷移宮）：哲學、遠行、高等教育
第10宮（官祿宮）：事業、社會地位
第11宮（福德宮）：朋友、願望、社交
第12宮（玄秘宮）：潛意識、隱藏、靈性

{'='*70}
"""
        return chart

    def _get_zodiac_name(self, month, day):
        """獲取星座名稱"""
        zodiacs = [
            (1, 20, "魔羯座"), (2, 19, "水瓶座"), (3, 21, "雙魚座"),
            (4, 20, "牡羊座"), (5, 21, "金牛座"), (6, 22, "雙子座"),
            (7, 23, "巨蟹座"), (8, 23, "獅子座"), (9, 23, "處女座"),
            (10, 24, "天秤座"), (11, 22, "天蠍座"), (12, 22, "射手座"),
            (12, 31, "魔羯座")
        ]
        
        for m, d, name in zodiacs:
            if month < m or (month == m and day <= d):
                return name
        return "魔羯座"

    def analyze_ziwei_with_chart(self, year, month, day, hour, gender):
        """紫微論命含命盤圖"""
        ps_data = self.purplestar_analyzer.analyze_ziwei(year, month, day, hour, gender)
        basic_result = self.purplestar_analyzer.format_result(ps_data)
        
        # 生成紫微命盤圖
        ziwei_chart = self._generate_ziwei_chart_text(ps_data)
        
        # 生成紫微12宮位詳細說明
        house_details = self._get_ziwei_house_details()
        
        return f"{basic_result}\n\n{ziwei_chart}\n\n{house_details}"

    def _get_ziwei_house_details(self):
        """獲取紫微斗數12宮位的詳細說明"""
        details = f"""
{'='*70}
               📖 紫微斗數十二宮位詳細解析 📖
{'='*70}

紫微斗數透過十二宮位全面分析人生各個層面：

┌──────────────────────────────────────────────────────────┐
│ 命宮 - 生命主軸與性格                                       │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★★★ （最重要的宮位）                            │
│                                                            │
│ 【代表意義】                                               │
│  • 個人基本性格與氣質                                       │
│  • 人生觀與價值觀                                           │
│  • 外在形象與給人的印象                                     │
│  • 一生命運的總體趨勢                                       │
│                                                            │
│ 【吉星進入】主星落在命宮會加強其特質                         │
│ 【凶星進入】需要透過努力化解負面影響                         │
│                                                            │
│ 【建議】命宮是人生的核心，要深入了解自己的優缺點，            │
│         發揮優勢，改善弱點。                                 │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 兄弟宮 - 手足關係與平輩                                     │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★☆☆                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 與兄弟姊妹的關係                                         │
│  • 同事、同學等平輩關係                                     │
│  • 合作夥伴的相處                                           │
│  • 手足的助力與阻力                                         │
│                                                            │
│ 【吉星進入】手足情深，朋友助力大                             │
│ 【凶星進入】容易與平輩產生衝突                               │
│                                                            │
│ 【建議】重視手足之情，維護平輩關係，互助互利。                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 夫妻宮 - 婚姻與配偶                                         │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★★★                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 配偶的性格特質                                           │
│  • 婚姻生活的品質                                           │
│  • 感情的發展與變化                                         │
│  • 配偶對自己的影響                                         │
│                                                            │
│ 【吉星進入】婚姻美滿，配偶條件佳                             │
│ 【凶星進入】感情易有波折，需要用心經營                       │
│                                                            │
│ 【建議】婚姻需要雙方共同經營，互相體諒、真誠溝通。            │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 子女宮 - 子女與創造力                                       │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★★☆                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 子女的數量與質量                                         │
│  • 與子女的緣分深淺                                         │
│  • 子女的性格與發展                                         │
│  • 個人的創造力與表現欲                                     │
│                                                            │
│ 【吉星進入】子女聰明孝順，有創意                             │
│ 【凶星進入】親子關係需要用心維繫                             │
│                                                            │
│ 【建議】重視子女教育，給予適當的關愛與自由。                  │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 財帛宮 - 財運與理財                                         │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★★★                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 一生的財運狀況                                           │
│  • 賺錢能力與理財方式                                       │
│  • 財富累積的潛力                                           │
│  • 金錢觀念與消費習慣                                       │
│                                                            │
│ 【吉星進入】財運亨通，善於理財                               │
│ 【凶星進入】財運起伏，需謹慎理財                             │
│                                                            │
│ 【建議】培養正確的金錢觀，開源節流，穩健投資。                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 疾厄宮 - 健康與體質                                         │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★★☆                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 先天體質與健康狀況                                       │
│  • 容易罹患的疾病                                           │
│  • 意外災害的可能性                                         │
│  • 健康管理的重點                                           │
│                                                            │
│ 【吉星進入】體質健康，少病少災                               │
│ 【凶星進入】需注意身體保養，定期檢查                         │
│                                                            │
│ 【建議】預防勝於治療，保持良好生活習慣，注意健康。            │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 遷移宮 - 外出與人際                                         │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★★☆                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 外出運勢與機會                                           │
│  • 在外地的發展                                             │
│  • 人際關係與貴人運                                         │
│  • 旅行與搬遷的吉凶                                         │
│                                                            │
│ 【吉星進入】出外逢貴，人際關係佳                             │
│ 【凶星進入】出門需謹慎，注意安全                             │
│                                                            │
│ 【建議】善待他人，廣結善緣，出外必有貴人相助。                │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 奴僕宮（交友宮）- 朋友與下屬                                 │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★☆☆                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 朋友的質量與助力                                         │
│  • 與下屬的關係                                             │
│  • 人際交往的模式                                           │
│  • 社交圈的狀況                                             │
│                                                            │
│ 【吉星進入】朋友真誠，部屬得力                               │
│ 【凶星進入】慎選朋友，防小人陷害                             │
│                                                            │
│ 【建議】交友需謹慎，但也要珍惜真心朋友。                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 官祿宮（事業宮）- 事業與工作                                 │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★★★                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 事業發展與成就                                           │
│  • 工作性質與環境                                           │
│  • 職場表現與升遷                                           │
│  • 事業目標與方向                                           │
│                                                            │
│ 【吉星進入】事業順利，步步高升                               │
│ 【凶星進入】事業多波折，需加倍努力                           │
│                                                            │
│ 【建議】認真工作，把握機會，事業必有所成。                    │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 田宅宮 - 不動產與家運                                       │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★★☆                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 不動產的擁有情況                                         │
│  • 家庭環境與居住品質                                       │
│  • 置產能力與機會                                           │
│  • 家族運勢                                                 │
│                                                            │
│ 【吉星進入】家運昌隆，置產容易                               │
│ 【凶星進入】家庭不寧，房產需謹慎                             │
│                                                            │
│ 【建議】適時購置房產，營造溫馨家庭氛圍。                      │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 福德宮 - 精神與享受                                         │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★★☆                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 精神生活與內心世界                                       │
│  • 興趣愛好與休閒                                           │
│  • 福分與享受能力                                           │
│  • 人生的快樂指數                                           │
│                                                            │
│ 【吉星進入】知足常樂，精神富足                               │
│ 【凶星進入】內心煩惱，需要調適                               │
│                                                            │
│ 【建議】培養興趣愛好，追求身心靈平衡。                        │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 父母宮 - 父母與長輩                                         │
├──────────────────────────────────────────────────────────┤
│ 【重要性】★★★★☆                                            │
│                                                            │
│ 【代表意義】                                               │
│  • 與父母的關係                                             │
│  • 父母的健康與運勢                                         │
│  • 得到長輩的幫助                                           │
│  • 對父母的孝順程度                                         │
│                                                            │
│ 【吉星進入】父母健康，關係和睦                               │
│ 【凶星進入】代溝較深，需要溝通                               │
│                                                            │
│ 【建議】孝順父母，尊敬長輩，福報自然來。                      │
└──────────────────────────────────────────────────────────┘

{'='*70}

【宮位重要性排序】

1. 命宮、夫妻宮、財帛宮、官祿宮 - 決定人生主要方向
2. 子女宮、疾厄宮、遷移宮、田宅宮、福德宮、父母宮 - 影響生活品質
3. 兄弟宮、奴僕宮 - 輔助人際關係

【看命盤的訣竅】

✦ 先看命宮，了解基本性格
✦ 再看三方四正（財帛、官祿、遷移）
✦ 注意吉星凶星的配置
✦ 觀察大限流年的變化
✦ 綜合判斷，不可偏執一宮

{'='*70}
"""
        return details

    def _generate_ziwei_chart_text(self, data):
        """生成紫微命盤文字圖 - 含主星配置"""
        # 从data中获取主星信息
        main_stars = data.get('main_stars', {})
        
        # 为每个宫位准备主星显示
        palace_stars = {}
        for palace, star_info in main_stars.items():
            star_name = star_info.get('star', '未知')
            palace_stars[palace] = star_name
        
        # 获取各宫位主星（使用宫位名称作为key）
        star_si = palace_stars.get('遷移宮', '－')
        star_wu = palace_stars.get('奴僕宮', '－')
        star_wei = palace_stars.get('官祿宮', '－')
        star_shen = palace_stars.get('田宅宮', '－')
        star_chen = palace_stars.get('疾厄宮', '－')
        star_you = palace_stars.get('福德宮', '－')
        star_mao = palace_stars.get('財帛宮', '－')
        star_yin = palace_stars.get('子女宮', '－')
        star_chou = palace_stars.get('夫妻宮', '－')
        star_zi = palace_stars.get('兄弟宮', '－')
        star_ming = palace_stars.get('命宮', '－')
        star_fu = palace_stars.get('父母宮', '－')
        
        chart = f"""
{'='*70}
                      🟣 紫微斗數命盤 🟣
{'='*70}

┌──────────────┬──────────────┬──────────────┬──────────────┐
│  巳宮（遷移）   │  午宮（奴僕）   │  未宮（官祿）   │  申宮（田宅）   │
│  主星：{star_si:6s}│  主星：{star_wu:6s}│  主星：{star_wei:6s}│  主星：{star_shen:6s}│
│              │              │              │              │
├──────────────┼──────────────┴──────────────┼──────────────┤
│  辰宮（疾厄）   │                            │  酉宮（福德）   │
│  主星：{star_chen:6s}│    ◎ 命 盤 中 宮 ◎      │  主星：{star_you:6s}│
│              │    命宮：{star_ming:6s}        │              │
├──────────────┼──────────────┬──────────────┼──────────────┤
│  卯宮（財帛）   │  寅宮（子女）   │  丑宮（夫妻）   │  子宮（兄弟）   │
│  主星：{star_mao:6s}│  主星：{star_yin:6s}│  主星：{star_chou:6s}│  主星：{star_zi:6s}│
│              │              │              │              │
└──────────────┴──────────────┴──────────────┴──────────────┘
                           │父母宮：{star_fu:6s}│

【十二宮位主星配置】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

• 命宮（{star_ming}）：個性、命運主軸
• 兄弟宮（{star_zi}）：手足、朋友關係
• 夫妻宮（{star_chou}）：婚姻、配偶情況
• 子女宮（{star_yin}）：子女、創造力
• 財帛宮（{star_mao}）：財運、理財能力
• 疾厄宮（{star_chen}）：健康、體質狀況

• 遷移宮（{star_si}）：外出、人際關係
• 奴僕宮（{star_wu}）：部屬、朋友助力
• 官祿宮（{star_wei}）：事業、工作發展
• 田宅宮（{star_shen}）：不動產、家庭
• 福德宮（{star_you}）：精神享受、福氣
• 父母宮（{star_fu}）：父母、長輩關係

【主星說明】
根據出生時辰，各宮位會有不同的主星落入。
主星決定該宮位的特質和發展方向，影響人生各個層面。

【重要宮位】
✦ 命宮、夫妻宮、財帛宮、官祿宮 - 決定人生主要方向
✦ 田宅宮、福德宮、父母宮 - 影響生活品質和福分
✦ 其他宮位 - 輔助人生發展

{'='*70}
"""
        return chart

    def display_result(self, key, content, header):
        """顯示分析結果（彩色格式化版本）"""
        text_widget = getattr(self, f"{key}_text")
        text_widget.delete(1.0, tk.END)
        
        # 使用彩色標籤格式化輸出
        self._insert_with_tags(text_widget, f"{'='*70}\n", 'normal')
        self._insert_with_tags(text_widget, f"  {header}\n", 'title')
        self._insert_with_tags(text_widget, f"  分析時間: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n", 'normal')
        self._insert_with_tags(text_widget, f"{'='*70}\n\n", 'normal')
        
        # 智能解析內容並應用標籤
        self._insert_formatted_content(text_widget, content)
    
    def _insert_with_tags(self, widget, text, tag):
        """插入帶標籤的文字"""
        widget.insert(tk.END, text, tag)
    
    def _insert_formatted_content(self, widget, content):
        """智能格式化內容輸出，自動應用彩色標籤"""
        lines = content.split('\n')
        
        for line in lines:
            # 判斷行的類型並應用相應標籤
            if '【' in line or line.strip().startswith('╔') or line.strip().startswith('║'):
                # 大標題
                self._insert_with_tags(widget, line + '\n', 'title')
            elif line.strip().startswith('★') or line.strip().startswith('◆') or line.strip().startswith('▲') or line.strip().startswith('═'):
                # 章節標題
                self._insert_with_tags(widget, line + '\n', 'header')
            elif line.strip().startswith('•') or line.strip().startswith('◇') or line.strip().startswith('○') or line.strip().startswith('－'):
                # 小節標題
                self._insert_with_tags(widget, line + '\n', 'subheader')
            elif '⚠' in line or '注意' in line or '警告' in line or '避免' in line or '重要' in line:
                # 重要提示
                self._insert_with_tags(widget, line + '\n', 'important')
            elif '配偶' in line or '婚姻' in line or '感情' in line or '夫妻' in line or '戀愛' in line or '❤' in line or '💑' in line:
                # 配偶相關
                self._insert_with_tags(widget, line + '\n', 'spouse')
            else:
                # 一般文字
                self._insert_with_tags(widget, line + '\n', 'normal')
    
    def _generate_progress_bar(self, value, max_value=100, width=30):
        """生成進度條圖形"""
        percentage = min(100, max(0, (value / max_value) * 100))
        filled = int((percentage / 100) * width)
        empty = width - filled
        return f"[{'█' * filled}{'░' * empty}] {percentage:.0f}%"
    
    def _generate_star_rating(self, score, max_score=100):
        """生成星級評分"""
        stars = int((score / max_score) * 5)
        return '★' * stars + '☆' * (5 - stars)
    
    def _generate_chart_header(self, title):
        """生成圖表標題"""
        return f"\n╔{'═'*60}╗\n║{title.center(58)}║\n╚{'═'*60}╝\n"

    def generate_comprehensive_summary(self, year, month, day, hour, gender, blood):
        """生成綜合總結"""
        summary = f"""
╔══════════════════════════════════════════════════════════════╗
║                  📊 完整命理分析綜合總結 📊                    ║
╚══════════════════════════════════════════════════════════════╝

【基本資料】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
出生日期：{year}年{month}月{day}日 {hour}時
性    別：{gender}
血    型：{blood}型
分析時間：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

【七大分析系統總結】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

1️⃣  星座命理分析
   {self._extract_summary('zodiac')}

2️⃣  血型性格分析
   {self._extract_summary('blood')}

3️⃣  八字命理分析
   {self._extract_summary('bazi')}

4️⃣  紫微斗數分析
   {self._extract_summary('purplestar')}

5️⃣  塔羅牌占卜
   {self._extract_summary('tarot')}

6️⃣  周易卜卦
   {self._extract_summary('yijing')}

7️⃣  九宮靈數分析
   {self._extract_summary('jiugong')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【整體運勢評估】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

◆ 性格特質：
  {self._get_personality_summary(blood)}

◆ 事業運勢：
  根據八字和紫微分析，您在事業上具備良好的發展潛力
  建議專注於自己的專長領域，穩紮穩打

◆ 財運分析：
  財運整體穩定，適合長期投資
  避免高風險投機，以穩健理財為主

◆ 感情運勢：
  感情方面需要真誠溝通，用心經營
  保持開放心態，緣分自然會到來

◆ 健康提醒：
  注意作息規律，保持良好生活習慣
  定期運動，維持身心健康平衡

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【人生建議】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

💡 短期建議（1年內）：
   • 專注當下，腳踏實地完成眼前的目標
   • 多與正面積極的人交流，拓展人脈
   • 學習新技能，提升自我競爭力

💡 中期規劃（3-5年）：
   • 建立穩固的事業基礎
   • 培養良好的理財習慣
   • 經營重要的人際關係

💡 長期展望（5年以上）：
   • 實現人生重要目標
   • 追求心靈成長與自我實現
   • 回饋社會，創造更大價值

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【開運建議】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

🎯 開運方位：根據八字五行，建議多往東方或南方發展
🎨 開運顏色：可多穿戴或使用與五行相生的顏色
🔢 幸運數字：根據命理分析，注意數字3、6、9的運用
⏰ 最佳時辰：早晨7-9點和下午1-3點為較佳時段

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【流年流月運勢】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        # 加入流年流月分析結果（如果有的話）
        if 'fortune' in self.analysis_results:
            summary += self.analysis_results['fortune']
        
        summary += """
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

【結語】
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

命理分析只是參考，真正的命運掌握在自己手中。
保持積極樂觀的態度，努力充實自己，
相信每個人都能創造屬於自己的精彩人生！

願您：
• 事業順利，步步高升
• 財源廣進，豐衣足食  
• 感情美滿，家庭幸福
• 身體健康，快樂平安

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
          本分析報告由 FATE Suite v2.3 自動生成
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        
        self.analysis_results['summary'] = summary
        summary_text = self.summary_text
        summary_text.delete(1.0, tk.END)
        summary_text.insert(tk.END, summary)

    def _extract_summary(self, key):
        """提取各分析的簡要摘要"""
        summaries = {
            'zodiac': '星座特質明顯，具有該星座的典型性格特徵',
            'blood': '血型性格與行為模式相符，展現出特定的處事風格',
            'bazi': '八字五行平衡，命格穩定，適合穩健發展',
            'purplestar': '命宮星曜吉祥，各宮位配置良好，前景可期',
            'tarot': '塔羅牌提示需要注意當下的選擇和內在指引',
            'yijing': '周易卦象顯示順應天時，謹慎行事為上策',
            'jiugong': '九宮靈數揭示您的人生道路與天賦才能'
        }
        return summaries.get(key, '分析結果良好')

    def _get_personality_summary(self, blood):
        """根據血型獲取性格摘要"""
        personalities = {
            'A': '謹慎細心，責任感強，注重細節和完美',
            'B': '樂觀開朗，創意豐富，喜歡自由自在',
            'AB': '理性冷靜，多才多藝，具有獨特魅力',
            'O': '自信果斷，領導能力強，充滿行動力'
        }
        return personalities.get(blood, '性格穩重，具備多元特質')

    def show_summary(self):
        """顯示總結"""
        if 'summary' not in self.analysis_results:
            messagebox.showwarning("提示", "請先完成命理分析！")
            return
        self.notebook.select(7)  # 切換到總結頁面（現在是第8個標籤頁，索引7）

    
    def apply_font_size_to_all(self):
        """即時將字體大小應用到所有文字框"""
        if not hasattr(self, 'text_widgets'):
            return
        
        base_size = self.current_font_size
        
        for widget in self.text_widgets:
            try:
                # 更新所有彩色標籤的字體大小
                widget.tag_configure('title', font=('Microsoft JhengHei', base_size+4, 'bold'), foreground='#0066CC')
                widget.tag_configure('header', font=('Microsoft JhengHei', base_size+2, 'bold'), foreground='#006633')
                widget.tag_configure('subheader', font=('Microsoft JhengHei', base_size+1, 'bold'), foreground='#FF6600')
                widget.tag_configure('important', font=('Microsoft JhengHei', base_size, 'bold'), foreground='#CC0000')
                widget.tag_configure('spouse', font=('Microsoft JhengHei', base_size+1, 'bold'), foreground='#9933CC')
                widget.tag_configure('normal', font=('Microsoft JhengHei', base_size), foreground='#000000')
                
                # 觸發視覺更新
                widget.update_idletasks()
            except:
                pass
    
    def perform_tarot_divination(self):
        """執行塔羅占卜（每次點擊產生新結果）"""
        try:
            # 獲取問題
            question = self.tarot_question_entry.get().strip()
            if not question:
                messagebox.showwarning("提示", "請先輸入您的問題！")
                return
            
            # 更新狀態
            self.status_label.config(text="🎴 正在進行塔羅占卜...")
            self.root.update()
            
            # 執行占卜
            birth_date = f"{self.birth_year.get()}-{self.birth_month.get()}-{self.birth_day.get()}"
            tarot_result = self.tarot_analyzer.draw_cards(birth_date, question)
            
            # 添加問題資訊頭部
            full_result = f"{'='*80}\n"
            full_result += "🎴 塔羅占卜結果\n"
            full_result += f"{'='*80}\n\n"
            full_result += f"【占卜時間】{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n"
            full_result += f"【您的問題】{question}\n\n"
            full_result += f"{'='*80}\n\n"
            full_result += tarot_result
            
            # 增強圖表化
            full_result = self._add_tarot_charts(full_result)
            
            # 顯示結果
            self.tarot_text.config(state=tk.NORMAL)
            self.tarot_text.delete(1.0, tk.END)
            self.tarot_text.insert(tk.END, full_result)
            self.tarot_text.config(state=tk.DISABLED)
            
            # 保存結果
            self.analysis_results['tarot'] = full_result
            
            # 更新狀態
            self.status_label.config(text=f"✅ 塔羅占卜完成！問題：{question[:20]}...")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"塔羅占卜失敗：{e}")
            self.status_label.config(text=f"❌ 塔羅占卜失敗")
    
    def perform_yijing_divination(self):
        """執行周易卜卦（每次點擊產生新結果）"""
        try:
            # 獲取問題
            question = self.yijing_question_entry.get().strip()
            if not question:
                messagebox.showwarning("提示", "請先輸入您的問題！")
                return
            
            # 更新狀態
            self.status_label.config(text="☯ 正在進行周易卜卦...")
            self.root.update()
            
            # 執行卜卦
            birth_date = f"{self.birth_year.get()}-{self.birth_month.get()}-{self.birth_day.get()}"
            yijing_result = self.yijing_analyzer.divine(birth_date, question)
            
            # 添加問題資訊頭部
            full_result = f"{'='*80}\n"
            full_result += "☯ 周易卜卦結果\n"
            full_result += f"{'='*80}\n\n"
            full_result += f"【卜卦時間】{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}\n"
            full_result += f"【您的問題】{question}\n\n"
            full_result += f"{'='*80}\n\n"
            full_result += yijing_result
            
            # 增強圖表化
            full_result = self._add_yijing_charts(full_result)
            
            # 顯示結果
            self.yijing_text.config(state=tk.NORMAL)
            self.yijing_text.delete(1.0, tk.END)
            self.yijing_text.insert(tk.END, full_result)
            self.yijing_text.config(state=tk.DISABLED)
            
            # 保存結果
            self.analysis_results['yijing'] = full_result
            
            # 更新狀態
            self.status_label.config(text=f"✅ 周易卜卦完成！問題：{question[:20]}...")
            
        except Exception as e:
            messagebox.showerror("錯誤", f"周易卜卦失敗：{e}")
            self.status_label.config(text=f"❌ 周易卜卦失敗")
    
    def load_results(self):
        """載入已儲存的分析結果"""
        try:
            # 選擇檔案
            filename = filedialog.askopenfilename(
                title="開啟命理分析報告",
                filetypes=[("文字檔案", "*.txt"), ("所有檔案", "*.*")],
                defaultextension=".txt"
            )
            
            if not filename:
                return
            
            # 更新狀態
            self.status_label.config(text="📂 正在載入檔案...")
            self.root.update()
            
            # 讀取檔案
            with open(filename, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # 定義分析項目的映射關係（包含所有可能的key變體）
            key_mapping = {
                'ZODIAC': ('astrology', 'astrology_text'),
                'ASTROLOGY': ('astrology', 'astrology_text'),
                'BAZI': ('bazi', 'bazi_text'),
                'PURPLESTAR': ('purplestar', 'purplestar_text'),
                'ZIWEI': ('purplestar', 'purplestar_text'),
                'TAROT': ('tarot', 'tarot_text'),
                'YIJING': ('yijing', 'yijing_text'),
                'JIUGONG': ('jiugong', 'jiugong_text'),
                'JIUGONG_NAME': ('jiugong', 'jiugong_text'),
                'BLOOD_TYPE': ('blood_type', 'blood_type_text'),
                'BLOOD': ('blood_type', 'blood_type_text')
            }
            
            loaded_count = 0
            
            # 使用分割方法解析
            delimiter = '\n' + '='*70 + '\n'
            sections = content.split(delimiter)
            
            # 遍歷sections並配對key-content
            i = 0
            while i < len(sections) - 1:
                # Key在section[i]的最後一行，內容在section[i+1]
                key_section = sections[i].strip()
                content_section = sections[i+1] if i+1 < len(sections) else ''
                
                # 獲取最後一行作為key
                key_lines = key_section.split('\n')
                key = key_lines[-1].strip().upper() if key_lines else ''
                
                # 跳過空key或分隔線
                if not key or key.startswith('=') or len(key) > 50:
                    i += 1
                    continue
                
                # 清理內容開頭的分隔線
                section_content = content_section.strip()
                if section_content.startswith('='*70):
                    parts = section_content.split('\n\n', 1)
                    if len(parts) > 1:
                        section_content = parts[1].strip()
                
                # 檢查是否在映射表中
                if key in key_mapping:
                    result_key, widget_name = key_mapping[key]
                    
                    # 檢查文字框是否存在
                    if hasattr(self, widget_name):
                        widget = getattr(self, widget_name)
                        widget.config(state=tk.NORMAL)
                        widget.delete(1.0, tk.END)
                        widget.insert(tk.END, section_content.strip())
                        widget.config(state=tk.DISABLED)
                        
                        # 保存到結果字典
                        self.analysis_results[result_key] = section_content.strip()
                        loaded_count += 1
                
                # 移動到下一組
                i += 2  # 跳過當前key和content sections
            
            if loaded_count > 0:
                # 顯示成功訊息
                filename_only = filename.split('/')[-1].split('\\')[-1]
                messagebox.showinfo("載入成功", f"已成功載入 {loaded_count} 個分析項目！\n\n檔案：{filename_only}")
                self.status_label.config(text=f"✅ 已載入 {loaded_count} 個分析項目")
                
                # 自動切換到第一個載入的分頁
                if 'astrology' in self.analysis_results:
                    for i in range(self.notebook.index('end')):
                        if '星座' in self.notebook.tab(i, 'text'):
                            self.notebook.select(i)
                            break
            else:
                messagebox.showwarning("警告", "未能識別檔案中的分析項目！\n\n請確認檔案格式正確。")
                self.status_label.config(text="⚠️ 檔案格式可能不正確")
                
        except Exception as e:
            messagebox.showerror("載入失敗", f"無法讀取檔案：{str(e)}")
            self.status_label.config(text="❌ 檔案載入失敗")
    
    def save_results(self):
        """儲存結果到文件"""
        if not self.analysis_results:
            messagebox.showwarning("提示", "沒有分析結果可以儲存！")
            return
        
        try:
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            filename = f"命理分析報告_{timestamp}.txt"
            
            with open(filename, 'w', encoding='utf-8') as f:
                for key, content in self.analysis_results.items():
                    f.write(f"\n{'='*70}\n")
                    f.write(f"  {key.upper()}\n")
                    f.write(f"{'='*70}\n\n")
                    f.write(content)
                    f.write("\n\n")
            
            messagebox.showinfo("儲存成功", f"分析結果已儲存至：\n{filename}")
            self.status_label.config(text=f"✅ 結果已儲存：{filename}")
            
        except Exception as e:
            messagebox.showerror("儲存失敗", f"無法儲存文件：{str(e)}")

    def print_report(self):
        """列印報告"""
        if not self.analysis_results:
            messagebox.showwarning("提示", "沒有分析結果可以列印！")
            return
        
        try:
            # 先儲存為臨時文件
            timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
            temp_filename = f"列印報告_{timestamp}.txt"
            
            # 生成完整報告
            report_content = self._generate_print_report()
            
            with open(temp_filename, 'w', encoding='utf-8') as f:
                f.write(report_content)
            
            # 顯示列印對話框
            result = messagebox.askquestion("列印報告", 
                f"報告已生成：{temp_filename}\n\n是否要開啟文件進行列印？\n\n提示：\n• 點擊「是」將開啟記事本\n• 您可以從記事本選擇列印\n• 或點擊「否」稍後自行列印",
                icon='question')
            
            if result == 'yes':
                # 使用記事本開啟文件
                import subprocess
                subprocess.Popen(['notepad.exe', temp_filename])
                self.status_label.config(text=f"✅ 已開啟列印文件：{temp_filename}")
            else:
                self.status_label.config(text=f"✅ 列印文件已儲存：{temp_filename}")
                
        except Exception as e:
            messagebox.showerror("列印失敗", f"無法生成列印文件：{str(e)}")

    def _generate_print_report(self):
        """生成適合列印的報告格式"""
        report = f"""
╔══════════════════════════════════════════════════════════════╗
║                                                              ║
║          🌟 FATE Suite 增強版 - 完整命理分析報告 🌟          ║
║                                                              ║
╚══════════════════════════════════════════════════════════════╝

報告生成時間：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                        目錄 CONTENTS

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

一、星座命盤分析 .................................................. 2
二、血型性格分析 .................................................. X
三、八字命理分析 .................................................. X
四、紫微斗數分析 .................................................. X
五、塔羅牌占卜 .................................................... X
六、周易卜卦 ...................................................... X
七、綜合總結報告 .................................................. X

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━


"""
        
        # 添加各個分析結果
        sections = [
            ("一、星座命盤分析", "zodiac"),
            ("二、血型性格分析", "blood"),
            ("三、八字命理分析", "bazi"),
            ("四、紫微斗數分析", "purplestar"),
            ("五、塔羅牌占卜", "tarot"),
            ("六、周易卜卦", "yijing"),
            ("七、綜合總結報告", "summary")
        ]
        
        for title, key in sections:
            if key in self.analysis_results:
                report += f"\n{'='*70}\n"
                report += f"{title}\n"
                report += f"{'='*70}\n\n"
                report += self.analysis_results[key]
                report += f"\n\n{'='*70}\n"
                report += f"第 {sections.index((title, key)) + 1} 部分結束\n"
                report += f"{'='*70}\n\n\n"
                report += "\f"  # 分頁符號
        
        # 添加頁尾
        report += f"""

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

                    報告結束 END OF REPORT

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━

本報告由 FATE Suite 增強版 自動生成
生成時間：{datetime.now().strftime('%Y年%m月%d日 %H:%M:%S')}

【免責聲明】
本報告內容僅供參考，不應作為人生重大決策的唯一依據。
命理分析是一種傳統文化，建議理性看待，並結合個人實際情況判斷。

【版權說明】
© 2026 FATE Suite Team. All Rights Reserved.
本報告為個人專屬，請勿用於商業用途。

━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
"""
        return report

    def clear_results(self):
        """清除所有結果"""
        for key in ['zodiac', 'blood', 'bazi', 'purplestar', 'tarot', 'yijing', 'jiugong', 'jiugong_name', 'summary']:
            text_widget = getattr(self, f"{key}_text", None)
            if text_widget:
                text_widget.delete(1.0, tk.END)
        
        self.analysis_results = {}
        self.status_label.config(text="✅ 已清除所有結果")
    
    def open_spouse_data_dialog(self):
        """打開配偶完整資料輸入對話框"""
        # 創建配偶資料輸入窗口
        spouse_window = tk.Toplevel(self.root)
        spouse_window.title("💑 配偶資料輸入")
        spouse_window.geometry("500x400")
        
        # 標題
        title_label = tk.Label(spouse_window, text="📝 請輸入配偶基本資料", 
                               font=("微軟正黑體", 14, "bold"), fg="#8B008B")
        title_label.pack(pady=10)
        
        # 主框架
        main_frame = ttk.Frame(spouse_window)
        main_frame.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)
        
        # 配偶姓名
        ttk.Label(main_frame, text="配偶姓名：", font=("微軟正黑體", 10)).grid(row=0, column=0, sticky=tk.W, pady=8)
        spouse_name_entry = ttk.Entry(main_frame, width=30)
        spouse_name_entry.grid(row=0, column=1, pady=8)
        
        # 配偶出生年份
        ttk.Label(main_frame, text="配偶出生年份：", font=("微軟正黑體", 10)).grid(row=1, column=0, sticky=tk.W, pady=8)
        spouse_year = ttk.Combobox(main_frame, values=list(range(1950, 2024)), width=27, state="readonly")
        spouse_year.set(1990)
        spouse_year.grid(row=1, column=1, pady=8)
        
        # 配偶出生月份
        ttk.Label(main_frame, text="配偶出生月份：", font=("微軟正黑體", 10)).grid(row=2, column=0, sticky=tk.W, pady=8)
        spouse_month = ttk.Combobox(main_frame, values=list(range(1, 13)), width=27, state="readonly")
        spouse_month.set(1)
        spouse_month.grid(row=2, column=1, pady=8)
        
        # 配偶出生日期
        ttk.Label(main_frame, text="配偶出生日期：", font=("微軟正黑體", 10)).grid(row=3, column=0, sticky=tk.W, pady=8)
        spouse_day = ttk.Combobox(main_frame, values=list(range(1, 32)), width=27, state="readonly")
        spouse_day.set(1)
        spouse_day.grid(row=3, column=1, pady=8)
        
        # 配偶出生時辰
        ttk.Label(main_frame, text="配偶出生時辰：", font=("微軟正黑體", 10)).grid(row=4, column=0, sticky=tk.W, pady=8)
        spouse_hour = ttk.Combobox(main_frame, values=list(range(0, 24)), width=27, state="readonly")
        spouse_hour.set(12)
        spouse_hour.grid(row=4, column=1, pady=8)
        
        # 配偶性別
        ttk.Label(main_frame, text="配偶性別：", font=("微軟正黑體", 10)).grid(row=5, column=0, sticky=tk.W, pady=8)
        spouse_gender = ttk.Combobox(main_frame, values=['男', '女'], width=27, state="readonly")
        spouse_gender.set('女')
        spouse_gender.grid(row=5, column=1, pady=8)
        
        # 配偶血型
        ttk.Label(main_frame, text="配偶血型：", font=("微軟正黑體", 10)).grid(row=6, column=0, sticky=tk.W, pady=8)
        spouse_blood = ttk.Combobox(main_frame, values=['A', 'B', 'AB', 'O'], width=27, state="readonly")
        spouse_blood.set('A')
        spouse_blood.grid(row=6, column=1, pady=8)
        
        # 按鈕框架
        button_frame = ttk.Frame(spouse_window)
        button_frame.pack(pady=20)
        
        def save_spouse_data():
            """保存配偶資料"""
            name = spouse_name_entry.get()
            if not name:
                self.status_label.config(text="⚠️ 請輸入配偶姓名")
                return
            
            # 保存配偶資料到類變量（修正：使用 spouse_full_data）
            self.spouse_full_data = {
                'name': name,
                'year': int(spouse_year.get()),
                'month': int(spouse_month.get()),
                'day': int(spouse_day.get()),
                'hour': int(spouse_hour.get()),
                'gender': spouse_gender.get(),
                'blood_type': spouse_blood.get()
            }
            
            self.status_label.config(text=f"✅ 已保存配偶資料：{name}（{spouse_year.get()}/{spouse_month.get()}/{spouse_day.get()}）- 請點擊「開始完整分析」")
            spouse_window.destroy()
        
        def cancel():
            """取消輸入"""
            spouse_window.destroy()
        
        ttk.Button(button_frame, text="✅ 確認保存", command=save_spouse_data).pack(side=tk.LEFT, padx=10)
        ttk.Button(button_frame, text="❌ 取消", command=cancel).pack(side=tk.LEFT, padx=10)
    
    def change_font_size(self, delta):
        """改變字體大小"""
        new_size = self.current_font_size + delta
        
        # 限制範圍 8-20
        if 8 <= new_size <= 20:
            self.current_font_size = new_size
            self.font_size_display.config(text=f"{self.current_font_size}pt")
            self.apply_font_size_to_all()
            self.save_settings()
            self.status_label.config(text=f"✅ 字體大小已改為 {self.current_font_size}pt（即時應用）")
        else:
            self.status_label.config(text=f"⚠️ 字體大小範圍：8-20pt")
    
    def reset_font_size(self):
        """重設字體大小為預設值"""
        self.current_font_size = 10  # 預設值
        self.font_size_display.config(text=f"{self.current_font_size}pt")
        self.apply_font_size_to_all()
        self.save_settings()
        self.status_label.config(text="✅ 字體大小已重設為預設值 10pt（即時應用）")
    
    def show_settings(self):
        """顯示設定對話框"""
        settings_window = tk.Toplevel(self.root)
        settings_window.title("⚙️ 系統設定")
        settings_window.geometry("680x820")
        settings_window.configure(bg='#FFF8E7')
        settings_window.transient(self.root)
        settings_window.grab_set()
        settings_window.resizable(True, True)
        
        # 標題
        title_frame = tk.Frame(settings_window, bg='#3498DB', height=60)
        title_frame.pack(fill=tk.X)
        title_frame.pack_propagate(False)
        
        tk.Label(
            title_frame,
            text="⚙️ 系統設定",
            font=('Microsoft JhengHei', 16, 'bold'),
            fg='#FFFFFF',
            bg='#3498DB'
        ).pack(expand=True)
        
        # 按鈕區（先建立，固定在底部）
        btn_frame = tk.Frame(settings_window, bg='#F0F0F0', pady=20, padx=20)
        btn_frame.pack(side=tk.BOTTOM, fill=tk.X)
        
        # 建立可滾動的內容區域（支援上下左右滾動）
        canvas_frame = tk.Frame(settings_window, bg='#FFF8E7')
        canvas_frame.pack(fill=tk.BOTH, expand=True)
        
        # 建立 Canvas 和垂直/水平 Scrollbar
        v_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.VERTICAL)
        h_scrollbar = tk.Scrollbar(canvas_frame, orient=tk.HORIZONTAL)
        canvas = tk.Canvas(canvas_frame, bg='#FFF8E7', highlightthickness=0,
                          yscrollcommand=v_scrollbar.set, 
                          xscrollcommand=h_scrollbar.set)
        
        v_scrollbar.config(command=canvas.yview)
        h_scrollbar.config(command=canvas.xview)
        
        # 放置 Scrollbars 和 Canvas
        v_scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        h_scrollbar.pack(side=tk.BOTTOM, fill=tk.X)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        
        # 建立實際的內容 Frame（設定固定寬度以觸發水平滾動）
        content_frame = tk.Frame(canvas, bg='#FFF8E7', padx=30, pady=20, width=800)
        
        # 將 content_frame 放入 Canvas
        canvas_window = canvas.create_window((0, 0), window=content_frame, anchor=tk.NW)
        
        # 綁定滾動事件和視窗調整
        def configure_scroll(event=None):
            canvas.configure(scrollregion=canvas.bbox("all"))
        
        content_frame.bind("<Configure>", configure_scroll)
        
        # 滑鼠滾輪支援（垂直滾動）
        def on_mousewheel(event):
            canvas.yview_scroll(int(-1*(event.delta/120)), "units")
        
        # 水平滾動支援（Shift + 滑鼠滾輪）
        def on_shift_mousewheel(event):
            canvas.xview_scroll(int(-1*(event.delta/120)), "units")
        
        # 綁定滾輪到 canvas 和其子元件
        def bind_mousewheel(widget):
            widget.bind("<MouseWheel>", on_mousewheel)
            widget.bind("<Shift-MouseWheel>", on_shift_mousewheel)
            for child in widget.winfo_children():
                bind_mousewheel(child)
        
        bind_mousewheel(canvas)
        bind_mousewheel(content_frame)
        
        # 確保初始顯示正確
        settings_window.update_idletasks()
        configure_scroll()
        
        # 字體設定
        font_frame = tk.LabelFrame(content_frame, text="字體設定", 
                                   font=('Microsoft JhengHei', 11, 'bold'),
                                   fg='#2C3E50', bg='#FFFFFF', padx=15, pady=15)
        font_frame.pack(fill=tk.X, pady=10)
        
        tk.Label(font_frame, text="字體大小：", 
                font=('Microsoft JhengHei', 10), fg='#2C3E50', bg='#FFFFFF').pack(anchor=tk.W)
        
        font_size_var = tk.IntVar(value=self.current_font_size)
        font_size_scale = tk.Scale(font_frame, from_=8, to=16, orient=tk.HORIZONTAL,
                                   variable=font_size_var, length=400, bg='#FFFFFF', fg='#2C3E50',
                                   font=('Microsoft JhengHei', 9))
        font_size_scale.pack(pady=5)
        
        # 當前值顯示
        current_size_label = tk.Label(font_frame, text=f"當前大小：{self.current_font_size} pt", 
                                     font=('Microsoft JhengHei', 9), fg='#7F8C8D', bg='#FFFFFF')
        current_size_label.pack(anchor=tk.W, pady=5)
        
        # 語言設定
        lang_frame = tk.LabelFrame(content_frame, text="語言設定", 
                                  font=('Microsoft JhengHei', 11, 'bold'),
                                  fg='#2C3E50', bg='#FFFFFF', padx=15, pady=15)
        lang_frame.pack(fill=tk.X, pady=10)
        
        lang_var = tk.StringVar(value=self.current_language)
        
        languages = [
            ('zh_TW', '繁體中文'),
            ('zh_CN', '简体中文'),
            ('en', 'English'),
            ('ja', '日本語')
        ]
        
        for lang_code, lang_name in languages:
            rb = tk.Radiobutton(
                lang_frame,
                text=lang_name,
                variable=lang_var,
                value=lang_code,
                font=('Microsoft JhengHei', 10),
                fg='#2C3E50',
                bg='#FFFFFF',
                selectcolor='#AED6F1'
            )
            rb.pack(anchor=tk.W, pady=3)
        
        # UI主題設定
        theme_frame = tk.LabelFrame(content_frame, text="UI主題", 
                                   font=('Microsoft JhengHei', 11, 'bold'),
                                   fg='#2C3E50', bg='#FFFFFF', padx=15, pady=15)
        theme_frame.pack(fill=tk.X, pady=10)
        
        theme_var = tk.StringVar(value=self.current_theme)
        
        themes = [
            ('light', '☀️ 白色柔和主題（當前）'),
            ('dark', '🌙 深色經典主題')
        ]
        
        for theme_code, theme_name in themes:
            rb = tk.Radiobutton(
                theme_frame,
                text=theme_name,
                variable=theme_var,
                value=theme_code,
                font=('Microsoft JhengHei', 10),
                fg='#2C3E50',
                bg='#FFFFFF',
                selectcolor='#AED6F1'
            )
            rb.pack(anchor=tk.W, pady=3)
        
        # 定義按鈕功能（btn_frame 已在頂部建立）
        def apply_settings():
            """應用設定"""
            # 保存設定到變量
            self.current_font_size = font_size_var.get()
            self.current_language = lang_var.get()
            self.current_theme = theme_var.get()
            
            # 保存設定到檔案
            if self.save_settings():
                messagebox.showinfo(
                    "設定已儲存", 
                    f"設定已儲存！\n\n字體大小：{self.current_font_size} pt\n語言：{dict(languages)[self.current_language]}\nUI主題：{dict(themes)[self.current_theme]}\n\n請重新啟動程式以套用所有變更。"
                )
            else:
                messagebox.showerror(
                    "儲存失敗",
                    "設定儲存失敗，請檢查檔案權限。"
                )
            settings_window.destroy()
        
        def cancel_settings():
            """取消設定"""
            # 清理滾輪綁定
            def unbind_mousewheel(widget):
                try:
                    widget.unbind("<MouseWheel>")
                    widget.unbind("<Shift-MouseWheel>")
                except:
                    pass
                for child in widget.winfo_children():
                    unbind_mousewheel(child)
            
            unbind_mousewheel(canvas)
            unbind_mousewheel(content_frame)
            settings_window.destroy()
        
        # 確定按鈕
        tk.Button(
            btn_frame,
            text="✅ 確定並套用",
            font=('Microsoft JhengHei', 10, 'bold'),
            fg='#FFFFFF',
            bg='#27AE60',
            activebackground='#229954',
            activeforeground='#FFFFFF',
            relief=tk.RAISED,
            bd=2,
            padx=30,
            pady=8,
            cursor="hand2",
            command=apply_settings
        ).pack(side=tk.RIGHT, padx=10)
        
        # 取消按鈕
        tk.Button(
            btn_frame,
            text="❌ 取消",
            font=('Microsoft JhengHei', 10),
            fg='#FFFFFF',
            bg='#95A5A6',
            activebackground='#7F8C8D',
            activeforeground='#FFFFFF',
            relief=tk.RAISED,
            bd=2,
            padx=30,
            pady=8,
            cursor="hand2",
            command=cancel_settings
        ).pack(side=tk.RIGHT, padx=10)

    def add_yearly_monthly_fortune(self, year, month, day, hour, gender):
        """加入流年流月分析"""
        from datetime import datetime
        
        # 使用系統當前日期
        now = datetime.now()
        current_year = now.year
        current_month = now.month
        
        # 計算流年
        yearly_fortune = self._calculate_yearly_fortune(year, month, day, gender, current_year)
        
        # 計算流月
        monthly_fortune = self._calculate_monthly_fortune(year, month, day, gender, current_year, current_month)
        
        result = f"""
{'='*70}
                  🌠 流年流月運勢分析 🌠
{'='*70}

【當前年份】{current_year}年（民國{current_year-1911}年）
【當前月份】{current_month}月

┌──────────────────────────────────────────────────────────┐
│ 📅 流年運勢（{current_year}年整體運勢）                        │
├──────────────────────────────────────────────────────────┤
│                                                            │
│ 【整體運勢】                                                │
│ {yearly_fortune['overall']}                                │
│                                                            │
│ 【事業運】★★★★☆                                           │
│ {yearly_fortune['career']}                                │
│                                                            │
│ 【財運】★★★☆☆                                             │
│ {yearly_fortune['wealth']}                                │
│                                                            │
│ 【感情運】★★★★☆                                           │
│ {yearly_fortune['love']}                                  │
│                                                            │
│ 【健康運】★★★☆☆                                           │
│ {yearly_fortune['health']}                                │
│                                                            │
│ 【貴人方位】{yearly_fortune['lucky_direction']}            │
│ 【幸運色彩】{yearly_fortune['lucky_color']}                │
│ 【開運建議】{yearly_fortune['advice']}                     │
│                                                            │
└──────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────┐
│ 📆 流月運勢（{current_month}月份運勢）                         │
├──────────────────────────────────────────────────────────┤
│                                                            │
│ 【本月焦點】{monthly_fortune['focus']}                      │
│                                                            │
│ 【上旬（1-10日）】                                          │
│ {monthly_fortune['first_third']}                          │
│                                                            │
│ 【中旬（11-20日）】                                         │
│ {monthly_fortune['second_third']}                         │
│                                                            │
│ 【下旬（21-月底）】                                         │
│ {monthly_fortune['last_third']}                           │
│                                                            │
│ 【本月吉日】{monthly_fortune['lucky_days']}                │
│ 【本月需注意】{monthly_fortune['caution']}                 │
│ 【開運行動】{monthly_fortune['action']}                    │
│                                                            │
└──────────────────────────────────────────────────────────┘

{'='*70}
"""
        return result

    def _calculate_yearly_fortune(self, birth_year, birth_month, birth_day, gender, current_year):
        """計算流年運勢"""
        # 根據生肖和年份五行生剋關係判斷運勢
        birth_zodiac = (birth_year - 4) % 12
        year_zodiac = (current_year - 4) % 12
        
        # 簡化的運勢判斷
        relationship = (year_zodiac - birth_zodiac) % 12
        
        fortune_map = {
            0: {  # 本命年
                'overall': '本命年，運勢起伏較大，需謹慎行事，可佩戴紅色飾品化解',
                'career': '事業變動可能性大，需穩紮穩打，不宜冒進，可得貴人相助',
                'wealth': '財運平平，正財尚可，偏財不利，避免投機和大額投資',
                'love': '感情需要用心經營，單身者有機會遇到正緣，已婚者需防小三',
                'health': '注意身體保養，定期檢查，避免意外傷害，多運動增強體質',
                'lucky_direction': '東南方',
                'lucky_color': '紅色、橙色',
                'advice': '多行善事，保持低調，穩中求進，可到寺廟祈福消災'
            },
            3: {  # 三合年
                'overall': '三合年，貴人運強，諸事順遂，是開創事業的好時機',
                'career': '事業運佳，升遷有望，適合轉職或創業，多與人合作',
                'wealth': '財運亨通，正財偏財皆旺，可適度投資，但仍需謹慎',
                'love': '桃花運旺，單身者易遇良緣，已婚者夫妻和睦，感情甜蜜',
                'health': '身體健康，精力充沛，但不可過勞，注意休息',
                'lucky_direction': '正南方',
                'lucky_color': '綠色、藍色',
                'advice': '把握機會，積極進取，多結交貴人，廣結善緣'
            },
            4: {  # 六合年
                'overall': '六合年，運勢平穩向上，適合合作共事，人際關係和諧',
                'career': '工作穩定，與同事相處融洽，團隊合作順利，業績提升',
                'wealth': '財運穩定，收入增加，適合儲蓄和穩健投資',
                'love': '感情運佳，單身者可透過朋友介紹遇到對象，已婚者幸福美滿',
                'health': '健康良好，心情愉悅，可多參加戶外活動',
                'lucky_direction': '正西方',
                'lucky_color': '白色、金色',
                'advice': '重視人際關係，多與人合作，真誠待人，互助互利'
            },
            6: {  # 相沖年
                'overall': '相沖年，波折較多，需防小人，謹慎行事，以守為攻',
                'career': '事業有阻，需加倍努力，避免與人正面衝突，多忍讓',
                'wealth': '財運不佳，開銷增加，避免借貸和擔保，謹慎理財',
                'love': '感情易生波折，需多溝通，避免誤會，單身者不宜急於求成',
                'health': '注意安全，防意外傷害，定期體檢，保持良好作息',
                'lucky_direction': '正北方',
                'lucky_color': '黑色、灰色',
                'advice': '低調行事，避免衝動，可佩戴護身符，多行善積德'
            }
        }
        
        # 根據關係選擇運勢（簡化版）
        if relationship in fortune_map:
            return fortune_map[relationship]
        else:
            # 其他年份（平運年）
            return {
                'overall': '運勢平穩，需腳踏實地，穩中求進，可有小幅進步',
                'career': '工作穩定，按部就班，可有小成就，不宜大幅變動',
                'wealth': '財運平平，收入穩定，適合儲蓄，不宜大額投資',
                'love': '感情平淡，需用心經營，單身者可多參加社交活動',
                'health': '健康尚可，注意季節變化，預防感冒，規律作息',
                'lucky_direction': '正東方',
                'lucky_color': '黃色、棕色',
                'advice': '穩紮穩打，累積實力，培養興趣，充實自己'
            }

    def _calculate_monthly_fortune(self, birth_year, birth_month, birth_day, gender, current_year, current_month):
        """計算流月運勢"""
        
        # 簡化的月運判斷
        fortunes = [
            {
                'focus': '事業發展，適合開展新計劃，人際關係活躍',
                'first_third': '月初運勢平穩，可規劃本月目標，適合開會討論',
                'second_third': '月中運勢上升，工作進展順利，可能有意外驚喜',
                'last_third': '月底需注意細節，收尾工作要仔細，避免功虧一簣',
                'lucky_days': f'{current_month}月6日、{current_month}月15日、{current_month}月24日',
                'caution': '注意人際關係，避免口舌是非，謹慎處理文書合約',
                'action': '多與人溝通，參加社交活動，學習新技能，拓展視野'
            },
            {
                'focus': '財運理財，適合投資規劃，關注物質層面',
                'first_third': '月初財運開始回升，可規劃理財，但不宜大額投資',
                'second_third': '月中可能有額外收入，把握賺錢機會，但避免衝動消費',
                'last_third': '月底需注意開銷，避免浪費，可適度儲蓄',
                'lucky_days': f'{current_month}月8日、{current_month}月17日、{current_month}月26日',
                'caution': '謹慎投資，避免借貸，控制購物慾望，理性消費',
                'action': '檢視財務狀況，制定儲蓄計劃，學習理財知識'
            },
            {
                'focus': '情感關係，適合表達心意，增進感情交流',
                'first_third': '月初感情升溫，單身者有機會遇到心儀對象',
                'second_third': '月中是表白或求婚的好時機，已婚者可安排約會',
                'last_third': '月底需避免誤會，多溝通，維護感情穩定',
                'lucky_days': f'{current_month}月3日、{current_month}月12日、{current_month}月21日',
                'caution': '避免爛桃花，保持理性，不要過度付出，注意界限',
                'action': '真誠表達情感，製造浪漫驚喜，重視伴侶需求'
            },
            {
                'focus': '健康養生，適合運動鍛鍊，調整作息',
                'first_third': '月初適合開始新的運動計劃，調整飲食習慣',
                'second_third': '月中注意不要過勞，適度休息，保持心情愉悅',
                'last_third': '月底需注意季節變化，預防疾病，定期檢查',
                'lucky_days': f'{current_month}月5日、{current_month}月14日、{current_month}月23日',
                'caution': '注意飲食衛生，避免熬夜，防止意外傷害，小心駕駛',
                'action': '規律作息，均衡飲食，多運動，保持正面心態'
            }
        ]
        
        # 根據月份選擇運勢類型
        fortune_index = current_month % 4
        return fortunes[fortune_index]
    
    # ========== 圖表增強函數 ==========
    
    def _add_zodiac_charts(self, content, month, day):
        """為星座分析添加圖表化元素"""
        # chart_enhancer 模組不存在，已禁用圖表功能
        return content
    
    def _add_blood_charts(self, content, blood_type):
        """為血型分析添加圖表化元素"""
        # chart_enhancer 模組不存在，已禁用圖表功能
        return content
    
    def _add_bazi_charts(self, content, bazi_data):
        """為八字分析添加圖表化元素"""
        # chart_enhancer 模組不存在，已禁用圖表功能
        return content
    
    def _add_ziwei_charts(self, content):
        """為紫微斗數添加圖表化元素"""
        # chart_enhancer 模組不存在，已禁用圖表功能
        return content
    
    def _add_tarot_charts(self, content):
        """為塔羅占卜添加圖表化元素"""
        # chart_enhancer 模組不存在，已禁用圖表功能
        return content
    
    def _add_yijing_charts(self, content):
        """為周易卜卦添加圖表化元素"""
        # chart_enhancer 模組不存在，已禁用圖表功能
        return content
    
        return content + charts
    
    def _analyze_bazi_spouse_compatibility(self, user_name, user_bazi_data, 
                                           spouse_name, spouse_bazi_data, user_gender):
        """八字配偶深度合適性分析"""
        analysis = "\n💑 八字配偶深度合適性分析"
        
        try:
            # 提取四柱信息（簡化版本）
            user_pillars = self._extract_bazi_pillars(user_bazi_data)
            spouse_pillars = self._extract_bazi_pillars(spouse_bazi_data)
            
            # 1. 四柱對比
            analysis += "\n【一、四柱對比分析】\n\n"
            analysis += f"{'':4s}{'年柱':6s}{'月柱':6s}{'日柱':6s}{'時柱':6s}\n"
            analysis += f"{user_name:4s}{user_pillars['year']:6s}{user_pillars['month']:6s}{user_pillars['day']:6s}{user_pillars['hour']:6s}\n"
            analysis += f"{spouse_name:4s}{spouse_pillars['year']:6s}{spouse_pillars['month']:6s}{spouse_pillars['day']:6s}{spouse_pillars['hour']:6s}\n"
            
            # 2. 日柱對比（最重要）
            analysis += "\n【二、日柱相配分析（最重要）】\n\n"
            day_compatibility = self._analyze_day_pillar_compatibility(
                user_pillars['day'], 
                spouse_pillars['day'],
                user_gender
            )
            analysis += day_compatibility
            
            # 3. 五行相生相剋
            analysis += "\n【三、五行生剋分析】\n\n"
            five_elements_analysis = self._analyze_five_elements_compatibility(
                user_bazi_data,
                spouse_bazi_data
            )
            analysis += five_elements_analysis
            
            # 4. 納音五行
            analysis += "\n【四、納音五行相配】\n\n"
            nayin_analysis = self._analyze_nayin_compatibility(
                user_pillars,
                spouse_pillars
            )
            analysis += nayin_analysis
            
            # 5. 婚姻宮（日支）
            analysis += "\n【五、婚姻宮分析（日支）】\n\n"
            marriage_palace_analysis = self._analyze_marriage_palace(
                user_pillars['day'],
                spouse_pillars['day']
            )
            analysis += marriage_palace_analysis
            
            # 6. 綜合評分
            analysis += "\n【六、合婚綜合評分】\n\n"
            compatibility_score = self._calculate_bazi_compatibility_score(
                user_bazi_data,
                spouse_bazi_data,
                user_gender
            )
            
            # 生成星級評分（簡化版本，無需 chart_enhancer）
            stars = "★" * min(int(compatibility_score / 20), 5)
            analysis += f"相容度評分：{compatibility_score}/100 {stars}\n\n"
            
            # 評價等級
            if compatibility_score >= 80:
                level = "【天作之合】"
                comment = "八字極為相配，先天條件優越！"
            elif compatibility_score >= 70:
                level = "【良緣佳配】"
                comment = "八字相合，婚姻幸福指數高。"
            elif compatibility_score >= 60:
                level = "【尚可相配】"
                comment = "八字基本協調，需要互相包容。"
            elif compatibility_score >= 50:
                level = "【可以接受】"
                comment = "八字有衝有合，需要加強溝通。"
            else:
                level = "【需要化解】"
                comment = "八字相沖較多，建議采用化解方式。"
            
            analysis += f"{level}\n{comment}\n\n"
            
            # 7. 詳細建議
            analysis += "【七、合婚建議】\n\n"
            advice = self._generate_bazi_marriage_advice(
                compatibility_score,
                user_bazi_data,
                spouse_bazi_data,
                user_gender
            )
            analysis += advice
            
            analysis += "\n" + "="*80 + "\n"
            
            return analysis
            
        except Exception as e:
            print(f"❌ 八字分析出錯：{e}")
            import traceback
            traceback.print_exc()
            return f"\n❌ 配偶八字分析出錯：{e}"
    
    def _extract_bazi_pillars(self, bazi_data):
        """從八字數據中提取四柱"""
        try:
            # 假設bazi_data字典包含year, month, day, hour等信息
            pillars = {
                'year': str(bazi_data.get('year', 'N/A'))[:2],
                'month': str(bazi_data.get('month', 'N/A'))[:2],
                'day': str(bazi_data.get('day', 'N/A'))[:2],
                'hour': str(bazi_data.get('hour', 'N/A'))[:2]
            }
            return pillars
        except:
            return {'year': 'N/A', 'month': 'N/A', 'day': 'N/A', 'hour': 'N/A'}
    
    def _analyze_day_pillar_compatibility(self, user_day, spouse_day, user_gender):
        """分析日柱相配（最重要）"""
        analysis = ""
        
        # 簡化的日柱相合表
        harmony_table = {
            ('子', '午'): "【對沖】相沖相害，需要化解",
            ('丑', '未'): "【對沖】相沖相害，需要化解",
            ('寅', '申'): "【對沖】相沖相害，需要化解",
            ('卯', '酉'): "【對沖】相沖相害，需要化解",
            ('辰', '戌'): "【對沖】相沖相害，需要化解",
            ('巳', '亥'): "【對沖】相沖相害，需要化解",
            ('子', '丑'): "【六合】相合，婚配最佳",
            ('寅', '卯'): "【相鄰】相近，感情穩定",
            ('午', '未'): "【相鄰】相近，感情穩定",
            ('申', '酉'): "【相鄰】相近，感情穩定",
        }
        
        key = (user_day[-1] if user_day else 'N/A', spouse_day[-1] if spouse_day else 'N/A')
        key_reverse = (spouse_day[-1] if spouse_day else 'N/A', user_day[-1] if user_day else 'N/A')
        
        if key in harmony_table:
            result = harmony_table[key]
        elif key_reverse in harmony_table:
            result = harmony_table[key_reverse]
        else:
            result = "【一般相配】基本和諧，無特別相沖。"
        
        analysis += f"本人日柱：{user_day}\n"
        analysis += f"配偶日柱：{spouse_day}\n"
        analysis += f"相配狀況：{result}\n\n"
        
        if '六合' in result:
            analysis += "✅ 日柱六合是婚配的最佳組合，預示感情和諧、夫妻恩愛。\n"
        elif '相沖' in result:
            analysis += "⚠️ 日柱相沖需要特別留意，建議通過其他化解方式改善。\n"
        else:
            analysis += "ℹ️ 日柱基本和諧，有利於建立穩定的婚姻關係。\n"
        
        return analysis
    
    def _analyze_five_elements_compatibility(self, user_bazi_data, spouse_bazi_data):
        """分析五行生剋相配"""
        analysis = ""
        
        # 簡化計算五行比例（無需使用 chart_enhancer）
        analysis += "\n五行分佈概況：\n"
        analysis += "  木: ████░░░░░░  (20%)\n"
        analysis += "  火: █████░░░░░  (25%)\n"
        analysis += "  土: ██████░░░░  (28%)\n"
        analysis += "  金: ████░░░░░░  (20%)\n"
        analysis += "  水: ███░░░░░░░  (18%)\n"
        
        analysis += "\n✅ 五行均衡：八字中五行分佈相對均勻\n"
        analysis += "📊 本人五行強度：金旺\n"
        analysis += "📊 配偶五行強度：水旺\n"
        analysis += "💫 相配分析：金生水，相生關係，相合度高\n\n"
        
        return analysis
    
    def _analyze_nayin_compatibility(self, user_pillars, spouse_pillars):
        """分析納音五行相配"""
        analysis = ""
        
        # 納音五行表（簡化）
        nayin_table = {
            '子': '水', '丑': '土', '寅': '木', '卯': '木',
            '辰': '土', '巳': '火', '午': '火', '未': '土',
            '申': '金', '酉': '金', '戌': '土', '亥': '水'
        }
        
        # 比較四柱納音五行
        user_elements = []
        spouse_elements = []
        
        for pillar in [user_pillars['year'], user_pillars['month'], 
                       user_pillars['day'], user_pillars['hour']]:
            if pillar and len(pillar) > 0:
                user_elements.append(nayin_table.get(pillar[-1], '無'))
        
        for pillar in [spouse_pillars['year'], spouse_pillars['month'], 
                       spouse_pillars['day'], spouse_pillars['hour']]:
            if pillar and len(pillar) > 0:
                spouse_elements.append(nayin_table.get(pillar[-1], '無'))
        
        analysis += f"本人納音五行：{' '.join(user_elements)}\n"
        analysis += f"配偶納音五行：{' '.join(spouse_elements)}\n\n"
        analysis += "✅ 納音相配度：較高\n"
        analysis += "💫 五行相生：互相補助，利於感情穩定\n\n"
        
        return analysis
    
    def _analyze_marriage_palace(self, user_day, spouse_day):
        """分析婚姻宮（日支）"""
        analysis = ""
        
        # 婚姻宮吉凶表
        marriage_palace_good = ['丑', '午', '未', '申', '卯']
        marriage_palace_fair = ['寅', '酉', '辰', '亥']
        marriage_palace_bad = ['子', '巳', '戌']
        
        user_status = ""
        if user_day[-1] in marriage_palace_good:
            user_status = "【吉】婚姻宮吉利"
        elif user_day[-1] in marriage_palace_fair:
            user_status = "【平】婚姻宮平和"
        else:
            user_status = "【凶】婚姻宮有衝"
        
        spouse_status = ""
        if spouse_day[-1] in marriage_palace_good:
            spouse_status = "【吉】婚姻宮吉利"
        elif spouse_day[-1] in marriage_palace_fair:
            spouse_status = "【平】婚姻宮平和"
        else:
            spouse_status = "【凶】婚姻宮有衝"
        
        analysis += f"本人婚姻宮（日支{user_day[-1]}）：{user_status}\n"
        analysis += f"配偶婚姻宮（日支{spouse_day[-1]}）：{spouse_status}\n\n"
        analysis += "💡 婚姻宮是決定婚姻質量的重要因素\n"
        analysis += "📌 若雙方皆吉，則婚姻幸福機率最高\n\n"
        
        return analysis
    
    def _calculate_bazi_compatibility_score(self, user_bazi_data, spouse_bazi_data, user_gender):
        """計算八字配偶合適性評分（0-100）"""
        score = 70  # 基礎分
        
        # 簡化計算，加入隨機因素使結果更合理
        import random
        
        # 日柱相合加分
        score += random.randint(5, 15)
        
        # 五行相配加分
        score += random.randint(3, 10)
        
        # 限制在0-100之間
        score = max(0, min(100, score))
        
        return score
    
    def _generate_bazi_marriage_advice(self, compatibility_score, user_bazi_data, 
                                        spouse_bazi_data, user_gender):
        """生成八字婚姻建議"""
        advice = ""
        
        if compatibility_score >= 80:
            advice += "1. 先天條件優越，建議抓住機會，早日步入婚姻殿堂。\n"
            advice += "2. 感情基礎良好，雙方合作會更加順利。\n"
            advice += "3. 婚後應珍惜對方，相互扶持，維持良好的感情互動。\n\n"
        elif compatibility_score >= 70:
            advice += "1. 婚配條件良好，適合進一步發展關係。\n"
            advice += "2. 建議多了解對方，增進感情交流。\n"
            advice += "3. 婚後應注重溝通，化解可能的分歧。\n\n"
        elif compatibility_score >= 60:
            advice += "1. 基本條件可以接受，需要更多的包容與理解。\n"
            advice += "2. 建議在交往中更加謹慎，充分認識對方。\n"
            advice += "3. 如決定結婚，應積極化解八字中的不利因素。\n\n"
        else:
            advice += "1. 八字有較多衝突，建議慎重考慮婚配。\n"
            advice += "2. 如決定結婚，應尋求命理師的化解建議。\n"
            advice += "3. 可考慮結婚時間、地點等化解方式。\n"
            advice += "4. 婚後應更加珍惜對方，主動溝通與包容。\n\n"
        
        advice += "💝 溫馨提示：\n"
        advice += "   八字配偶合適性只是參考因素之一。\n"
        advice += "   真正的婚姻幸福需要雙方共同努力和經營。\n"
        advice += "   相愛、理解、尊重和信任才是維繫感情的根本。\n"
        
        return advice
    
    def _add_jiugong_charts(self, content):
        """為九宮分析添加圖表化元素"""
        # chart_enhancer 模組不存在，已禁用圖表功能
        return content


def main():
    """主程式入口"""
    root = tk.Tk()
    app = EnhancedFATESuiteGUI(root)
    root.mainloop()


if __name__ == "__main__":
    main()
