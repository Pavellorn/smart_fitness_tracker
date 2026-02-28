"""
Главный файл приложения.
Запускает приложение и управляет экранами.
"""

from kivy.app import App
from kivy.core.window import Window
from kivy.uix.screenmanager import ScreenManager, SlideTransition

# Прямые импорты экранов
from screens.training_screen import TrainingScreen
from screens.stats_screen import StatsScreen
from screens.setting_screen import SettingsScreen


class FitnessApp(App):
    """
    Главный класс приложения.
    """
    
    def build(self):
        """
        Создание и настройка приложения.
        """
        # Размер окна
        Window.size = (400, 700)
        
        # Менеджер экранов
        sm = ScreenManager(transition=SlideTransition(duration=0.3))
        
        # Добавление экранов
        sm.add_widget(TrainingScreen(name='main'))
        sm.add_widget(StatsScreen(name='stats'))
        sm.add_widget(SettingsScreen(name='settings'))
        
        return sm


if __name__ == '__main__':
    FitnessApp().run()