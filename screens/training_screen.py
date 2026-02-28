"""
Экран тренировки.
Главный экран приложения.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

# Прямые импорты из файлов
from kv.background import Background
from kv.animated_circle import AnimatedCircle
from utils.constants import COLORS


class TrainingScreen(Screen):
    """
    Главный экран приложения - экран тренировки.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        # Корневой контейнер
        root = Background(
            orientation='vertical',
            padding=20,
            spacing=20
        )

        # Заголовок
        root.add_widget(Label(
            text='ТРЕНИРОВКА',
            font_size=32,
            color=COLORS['white'],
            bold=True,
            size_hint_y=0.1
        ))

        # Контейнер для круга
        circle_box = BoxLayout(size_hint_y=0.5)
        
        # Анимированный круг работает пока не очень но он старается
        self.circle = AnimatedCircle(
            size_hint=(None, None),
            size=(300, 300)
        )
        self.circle.pos_hint = {'center_x': 0.5}
        
        circle_box.add_widget(self.circle)
        root.add_widget(circle_box)

        # Кнопки выбора времени
        buttons = BoxLayout(spacing=10, size_hint_y=0.2)
        
        # 30 минут (зеленая)
        btn30 = Button(text='30 мин', background_color=COLORS['success'])
        btn30.bind(on_press=lambda x: self.on_time_selected(30))
        
        # 60 минут (оранжевая)
        btn60 = Button(text='60 мин', background_color=COLORS['warning'])
        btn60.bind(on_press=lambda x: self.on_time_selected(60))
        
        # 90 минут (красная)
        btn90 = Button(text='90 мин', background_color=COLORS['danger'])
        btn90.bind(on_press=lambda x: self.on_time_selected(90))
        
        buttons.add_widget(btn30)
        buttons.add_widget(btn60)
        buttons.add_widget(btn90)
        root.add_widget(buttons)

        # Навигационные стрелки
        arrows = BoxLayout(size_hint_y=0.1)
        
        left = Button(text='<--', font_size=30)
        left.bind(on_press=lambda x: self.go_to_screen('settings'))
        
        right = Button(text='-->', font_size=30)
        right.bind(on_press=lambda x: self.go_to_screen('stats'))
        
        arrows.add_widget(left)
        arrows.add_widget(right)
        root.add_widget(arrows)

        self.add_widget(root)
        
        # Начальный прогресс
        self.circle.update_progress(50)
    
    def on_time_selected(self, minutes):
        """Обработчик выбора времени."""
        print(f"Выбрано время: {minutes} минут")
        self.circle.update_progress(minutes)
    
    def go_to_screen(self, screen_name):
        """Переход на другой экран."""
        self.manager.current = screen_name