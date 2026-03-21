import os
import sys
from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import ScreenManager, SlideTransition
from kivy.factory import Factory

# Добавляем пути для импортов
sys.path.append(os.path.dirname(__file__))

# Импорты из бэкенда (логика)
from logic.storage_manager import StorageManager
from logic.workout_manager import WorkoutManager
from logic.stats_manager import StatsManager
from logic.settings_manager import SettingsManager

# Импорты из фронтенда (UI)
from frontend.screens import WorkoutScreen, StatsScreen, SettingsScreen
from frontend.widgets import WeekGraph, ProgressCircle


class SwipeScreenManager(ScreenManager):
    """Свайпы между экранами (из фронтенда)"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self._touch_start_x = 0
        self._touch_start_y = 0
        self._swipe_threshold = 80

    def on_touch_down(self, touch):
        self._touch_start_x = touch.x
        self._touch_start_y = touch.y
        return super().on_touch_down(touch)

    def on_touch_up(self, touch):
        dx = touch.x - self._touch_start_x
        dy = touch.y - self._touch_start_y

        if abs(dx) > self._swipe_threshold and abs(dx) > abs(dy):
            screen_order = ["workout", "stats", "settings"]
            current_index = screen_order.index(self.current)

            if dx < 0 and current_index < len(screen_order) - 1:
                self.transition.direction = "left"
                self.current = screen_order[current_index + 1]
                return True

            if dx > 0 and current_index > 0:
                self.transition.direction = "right"
                self.current = screen_order[current_index - 1]
                return True

        return super().on_touch_up(touch)


class UnifiedFitnessApp(App):
    """Объединенное приложение"""

    def build(self):
        # 1. Регистрируем кастомные виджеты из фронтенда
        Factory.register("WeekGraph", cls=WeekGraph)
        Factory.register("ProgressCircle", cls=ProgressCircle)

        # 2. ИНИЦИАЛИЗИРУЕМ БЭКЕНД (ГОТОВАЯ ЛОГИКА)
        self.storage = StorageManager()  # БЕЗ АРГУМЕНТОВ
        self.stats = StatsManager(self.storage)  # С ARG
        self.workout = WorkoutManager(self.storage, self.stats)  # С ARG
        self.settings = SettingsManager(self.storage)  # ТЕПЕРЬ РАБОТАЕТ!
        # 2.5 СБРОС НЕЗАВЕРШЁННОЙ ТРЕНИРОВКИ ПРИ ЗАПУСКЕ
        self.storage.reset_current_workout()
        self.storage.save()
        # 3. ЗАГРУЖАЕМ KV ФАЙЛЫ ИЗ ФРОНТЕНДА
        Builder.load_file(os.path.join("frontend", "workout.kv"))
        Builder.load_file(os.path.join("frontend", "statistic.kv"))
        Builder.load_file(os.path.join("frontend", "settings.kv"))

        # 4. СОЗДАЕМ ЭКРАНЫ ИЗ ФРОНТЕНДА
        workout_screen = WorkoutScreen(name="workout")
        stats_screen = StatsScreen(name="stats")
        settings_screen = SettingsScreen(name="settings")

        # 5. ПЕРЕДАЕМ БЭКЕНД В ЭКРАНЫ
        # WorkoutScreen
        workout_screen.storage = self.storage
        workout_screen.workout_manager = self.workout
        workout_screen.stats_manager = self.stats
        workout_screen.settings_manager = self.settings

        # StatsScreen
        stats_screen.storage = self.storage
        stats_screen.stats_manager = self.stats
        stats_screen.settings_manager = self.settings

        # SettingsScreen - ВАЖНО: передаем stats_manager для reset_week_only
        settings_screen.storage = self.storage
        settings_screen.settings_manager = self.settings
        settings_screen.stats_manager = self.stats  # ЭТО ВАЖНО!

        # 6. СОЗДАЕМ МЕНЕДЖЕР ЭКРАНОВ
        sm = SwipeScreenManager(transition=SlideTransition())
        sm.add_widget(workout_screen)
        sm.add_widget(stats_screen)
        sm.add_widget(settings_screen)

        return sm


if __name__ == "__main__":
    # Создаем папку для данных, если её нет
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    if not os.path.exists(data_dir):
        os.makedirs(data_dir)
        print(f"Создана папка: {data_dir}")

    UnifiedFitnessApp().run()
