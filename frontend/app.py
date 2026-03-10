from kivy.app import App
from kivy.lang import Builder
from kivy.uix.screenmanager import (
    ScreenManager,
    SlideTransition,
)
from frontend.screens import (
    WorkoutScreen,
    StatsScreen,
    SettingsScreen,
)
from kivy.factory import Factory

from frontend.widgets import (
    WeekGraph,
    ProgressCircle,
)


class SwipeScreenManager(ScreenManager):
    """Свайпов между экранами"""

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


class FitnessApp(App):
    """Главное приложение фитнес-трекера"""

    def build(self):
        # Регистрируем классы, чтобы KV-файлы их "видели"
        Factory.register("WeekGraph", cls=WeekGraph)
        Factory.register("ProgressCircle", cls=ProgressCircle)

        Builder.load_file("frontend/workout.kv")  # todo: нужно реализовать
        Builder.load_file("frontend/statistic.kv")
        Builder.load_file("frontend/settings.kv")

        sm = SwipeScreenManager(transition=SlideTransition())
        sm.add_widget(WorkoutScreen(name="workout"))  # todo: нужно реализовать
        sm.add_widget(StatsScreen(name="stats"))
        sm.add_widget(SettingsScreen(name="settings"))

        return sm
