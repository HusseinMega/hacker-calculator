# main.py - Professional Hacker Calculator

from kivy.app import App
from kivy.uix.floatlayout import FloatLayout
from kivy.properties import StringProperty, NumericProperty, ListProperty
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, Screen
from kivy.animation import Animation
from kivy.clock import Clock
from kivy.core.audio import SoundLoader
import math

# تعيين لون النافذة الافتراضي إلى الأسود
Window.clearcolor = (0, 0, 0, 1)

# --- الشاشة الافتتاحية (Splash Screen) المحسنة ---
class SplashScreen(Screen):
    """
    شاشة ترحيبية احترافية مع تأثيرات متقدمة
    """
    text_opacity = NumericProperty(0)
    glitch_offset = NumericProperty(0)

    def on_enter(self, *args):
        # تأثير الظهور التدريجي
        anim = Animation(text_opacity=1, duration=1.2)
        anim.bind(on_complete=self.start_glitch_effect)
        anim.start(self)

    def start_glitch_effect(self, *args):
        # تأثير glitch بسيط
        for i in range(5):
            Clock.schedule_once(lambda dt, i=i: self.glitch(), i * 0.1)
        Clock.schedule_once(self.start_fade_out, 1.5)

    def glitch(self):
        # تأثير اهتزاز خفيف
        anim = Animation(glitch_offset=5, duration=0.05) + Animation(glitch_offset=0, duration=0.05)
        anim.start(self)

    def start_fade_out(self, *args):
        Clock.schedule_once(self.fade_out, 1)

    def fade_out(self, *args):
        anim = Animation(text_opacity=0, duration=1)
        anim.bind(on_complete=self.go_to_calculator)
        anim.start(self)

    def go_to_calculator(self, *args):
        self.manager.current = 'calculator'


# --- شاشة الآلة الحاسبة ---
class CalculatorScreen(Screen):
    pass


# --- الودجت الرئيسي للآلة الحاسبة المحترفة ---
class CalculatorWidget(FloatLayout):
    """
    آلة حاسبة احترافية مع ميزات متقدمة
    """
    display_text = StringProperty("0")
    history_text = StringProperty("")
    memory_value = NumericProperty(0)
    is_new_calculation = False
    calculation_history = ListProperty([])
    
    # ألوان ديناميكية
    display_color = ListProperty([0, 1, 0, 1])
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.last_result = 0
        
    def on_button_press(self, button_text):
        """
        معالجة متقدمة لضغطات الأزرار
        """
        current_text = self.display_text
        operators = "+-×÷"
        
        # أزرار المسح
        if button_text == "C":
            self.clear_all()
            self.animate_display_color([0, 1, 0, 1])
        
        elif button_text == "CE":
            self.display_text = "0"
            self.animate_display_color([0, 1, 0, 1])
        
        elif button_text == "←":
            self.backspace()
        
        # أزرار الذاكرة
        elif button_text == "MC":
            self.memory_value = 0
            self.show_notification("Memory Cleared")
        
        elif button_text == "MR":
            if self.memory_value != 0:
                self.display_text = str(self.memory_value)
                self.show_notification(f"Memory: {self.memory_value}")
        
        elif button_text == "M+":
            try:
                self.memory_value += float(self.display_text)
                self.show_notification(f"Memory: {self.memory_value}")
            except:
                pass
        
        elif button_text == "M-":
            try:
                self.memory_value -= float(self.display_text)
                self.show_notification(f"Memory: {self.memory_value}")
            except:
                pass
        
        # دوال علمية متقدمة
        elif button_text == "√":
            self.apply_function(lambda x: math.sqrt(x), "√")
        
        elif button_text == "x²":
            self.apply_function(lambda x: x ** 2, "²")
        
        elif button_text == "1/x":
            self.apply_function(lambda x: 1 / x, "⁻¹")
        
        elif button_text == "%":
            self.apply_percentage()
        
        elif button_text == "±":
            self.toggle_sign()
        
        # زر المساواة
        elif button_text == "=":
            self.calculate_result()
        
        # المعاملات
        elif button_text in operators:
            self.handle_operator(button_text)
        
        # الأرقام والنقطة
        else:
            self.handle_number_input(button_text)
    
    def clear_all(self):
        """مسح كامل"""
        self.display_text = "0"
        self.history_text = ""
        self.is_new_calculation = False
    
    def backspace(self):
        """حذف آخر رقم"""
        if self.display_text != "ERROR" and len(self.display_text) > 1:
            self.display_text = self.display_text[:-1]
        else:
            self.display_text = "0"
    
    def handle_number_input(self, button_text):
        """معالجة إدخال الأرقام"""
        if button_text == '.' and '.' in self.display_text:
            return
        
        if self.display_text == "0" or self.display_text == "ERROR" or self.is_new_calculation:
            self.display_text = button_text
            self.is_new_calculation = False
        else:
            self.display_text += button_text
    
    def handle_operator(self, operator):
        """معالجة المعاملات"""
        if self.display_text == "ERROR":
            return
        
        current_text = self.display_text
        if current_text and current_text[-1] not in "+-×÷":
            self.display_text += operator
            self.is_new_calculation = False
    
    def apply_function(self, func, symbol):
        """تطبيق دالة رياضية"""
        try:
            value = float(self.display_text)
            result = func(value)
            
            # تنسيق النتيجة
            if abs(result) < 0.0001 and result != 0:
                result_str = f"{result:.10e}"
            else:
                result_str = f"{result:.10f}".rstrip('0').rstrip('.')
            
            self.history_text = f"{symbol}({value}) ="
            self.display_text = result_str
            self.is_new_calculation = True
            self.animate_display_color([0, 1, 1, 1])  # أزرق سماوي
            
        except Exception as e:
            self.display_text = "ERROR"
            self.animate_display_color([1, 0, 0, 1])
    
    def apply_percentage(self):
        """حساب النسبة المئوية"""
        try:
            value = float(self.display_text)
            result = value / 100
            self.display_text = str(result)
            self.is_new_calculation = True
        except:
            self.display_text = "ERROR"
    
    def toggle_sign(self):
        """تبديل الإشارة"""
        try:
            if self.display_text != "0" and self.display_text != "ERROR":
                value = float(self.display_text)
                self.display_text = str(-value)
        except:
            pass
    
    def calculate_result(self):
        """حساب النتيجة النهائية"""
        if self.display_text == "0" or self.display_text == "ERROR":
            return
        
        try:
            expression = self.display_text.replace('×', '*').replace('÷', '/')
            result = eval(expression)
            
            # تنسيق النتيجة
            if '.' in str(result):
                result_str = f"{float(result):.10f}".rstrip('0').rstrip('.')
            else:
                result_str = str(result)
            
            # حفظ في السجل
            self.calculation_history.append(f"{self.display_text} = {result_str}")
            if len(self.calculation_history) > 10:
                self.calculation_history.pop(0)
            
            self.history_text = self.display_text + " ="
            self.display_text = result_str
            self.last_result = float(result_str)
            self.is_new_calculation = True
            
            # تأثير بصري للنجاح
            self.animate_display_color([0, 1, 0, 1])
            
        except ZeroDivisionError:
            self.display_text = "Cannot ÷ 0"
            self.animate_display_color([1, 0.5, 0, 1])
        except Exception:
            self.display_text = "ERROR"
            self.animate_display_color([1, 0, 0, 1])
    
    def show_notification(self, message):
        """عرض إشعار في التاريخ"""
        self.history_text = message
        Clock.schedule_once(lambda dt: setattr(self, 'history_text', ''), 2)
    
    def animate_display_color(self, target_color):
        """تأثير تغيير لون العرض"""
        anim = Animation(display_color=target_color, duration=0.3)
        anim.start(self)


# --- فئة التطبيق الرئيسية ---
class HackerCalculatorApp(App):
    """
    تطبيق آلة حاسبة احترافي بتصميم هاكر
    """
    def build(self):
        sm = ScreenManager()
        sm.add_widget(SplashScreen(name='splash'))
        sm.add_widget(CalculatorScreen(name='calculator'))
        return sm


# --- نقطة انطلاق التطبيق ---
if __name__ == "__main__":
    HackerCalculatorApp().run()
