"""
Экран настроек.
Позволяет настроить параметры приложения.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.button import Button
from kivy.uix.slider import Slider
from kivy.uix.togglebutton import ToggleButton

from kv.background import Background
from utils.constants import COLORS, GOAL_SLIDER


class SettingsScreen(Screen):
    """
    Экран настроек приложения.
    """
    
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        
        root = Background(
            orientation='vertical',
            padding=20,
            spacing=20
        )

        # Заголовок
        root.add_widget(Label(
            text='НАСТРОЙКИ',
            font_size=32,
            color=COLORS['white'],
            bold=True,
            size_hint_y=0.1
        ))

        # Контейнер настроек
        box = BoxLayout(
            orientation='vertical',
            spacing=20,
            size_hint_y=0.6
        )

        # Настройка цели
        goal = BoxLayout(orientation='vertical')
        goal.add_widget(Label(text='Цель (мин/неделя):', font_size=18))
        
        self.goal_slider = Slider(
            min=GOAL_SLIDER['min'],
            max=GOAL_SLIDER['max'],
            value=GOAL_SLIDER['default']
        )
        self.goal_slider.bind(value=self.on_goal_change)
        
        self.goal_value = Label(
            text=f"{GOAL_SLIDER['default']} мин",
            color=COLORS['accent']
        )
        
        goal.add_widget(self.goal_slider)
        goal.add_widget(self.goal_value)
        box.add_widget(goal)

        # Настройка уведомлений
        notify = BoxLayout(orientation='vertical')
        notify.add_widget(Label(text='Уведомления:', font_size=18))
        
        self.notify_toggle = ToggleButton(text='ON', state='down')
        self.notify_toggle.bind(state=self.on_notify_toggle)
        notify.add_widget(self.notify_toggle)
        box.add_widget(notify)

        # Настройка темы
        theme = BoxLayout(orientation='vertical')
        theme.add_widget(Label(text='Тема:', font_size=18))
        
        self.theme_toggle = ToggleButton(text='Тёмная')
        self.theme_toggle.bind(state=self.on_theme_toggle)
        theme.add_widget(self.theme_toggle)
        box.add_widget(theme)

        root.add_widget(box)

        # Кнопки управления
        btns = BoxLayout(size_hint_y=0.15, spacing=10)
        btns.add_widget(Button(
            text='Сохранить',
            background_color=COLORS['success']
        ))
        btns.add_widget(Button(
            text='Сбросить',
            background_color=COLORS['danger']
        ))
        root.add_widget(btns)

        # Кнопка возврата
        back = Button(
            text='← Назад',
            size_hint=(0.4, 0.1),
            pos_hint={'center_x': 0.5}
        )
        back.bind(on_press=lambda x: self.go_to_main())
        root.add_widget(back)

        self.add_widget(root)
    
    def on_goal_change(self, instance, value):
        """Обновление значения цели."""
        self.goal_value.text = f"{int(value)} мин"
    
    def on_notify_toggle(self, instance, state):
        """Переключение уведомлений."""
        instance.text = 'ON' if state == 'down' else 'OFF'
        instance.background_color = (
            COLORS['success'] if state == 'down' else COLORS['danger']
        )
    
    def on_theme_toggle(self, instance, state):
        """Переключение темы."""
        instance.text = 'Тёмная' if state == 'down' else 'Светлая'
    
    def go_to_main(self):
        """Переход на главный экран."""
        self.manager.current = 'main'