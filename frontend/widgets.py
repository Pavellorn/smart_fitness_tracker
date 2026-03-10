from datetime import datetime

from kivy.clock import Clock
from kivy.graphics import (
    Color,
    Line,
    Rectangle,
)
from kivy.metrics import dp
from kivy.properties import (
    NumericProperty,
    ListProperty,
    BooleanProperty,
)
from kivy.uix.widget import Widget


class ProgressCircle(Widget):
    progress_angle = NumericProperty(0)
    line_width = NumericProperty(14)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw, size=self.draw, progress_angle=self.draw)
        Clock.schedule_once(self.draw, 0)

    def draw(self, *args):
        self.canvas.after.clear()
        cx = self.center_x
        cy = self.center_y
        r = min(self.width, self.height) / 2 - self.line_width

        if r <= 0:
            return

        with self.canvas.after:
            Color(0.85, 0.85, 0.85, 1)
            Line(circle=(cx, cy, r, 0, 360), width=self.line_width, cap="round")

            if self.progress_angle > 0:
                Color(0.298, 0.686, 0.314, 1)
                Line(
                    circle=(cx, cy, r, 0, self.progress_angle),
                    width=self.line_width,
                    cap="round",
                )


class WeekGraph(Widget):
    values = ListProperty([0, 0, 0, 0, 0, 0, 0])
    highlight_today = BooleanProperty(True)

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.bind(pos=self.draw, size=self.draw, values=self.draw)
        Clock.schedule_once(self.draw, 0.1)

    def draw(self, *args):
        self.canvas.after.clear()

        if not self.values:
            return

        max_val = max(self.values) if max(self.values) > 0 else 1
        count = len(self.values)
        spacing = dp(8)
        bar_width = (self.width - spacing * (count + 1)) / count

        if bar_width <= 0:
            return

        today_index = datetime.now().weekday()

        with self.canvas.after:
            for i, val in enumerate(self.values):
                x = self.x + spacing + i * (bar_width + spacing)

                if val > 0:
                    height = (val / max_val) * self.height * 0.85
                else:
                    height = dp(3)

                if self.highlight_today and i == today_index:
                    Color(1.0, 0.596, 0.0, 1)
                elif val == 0:
                    Color(0.85, 0.85, 0.85, 1)
                else:
                    ratio = val / max_val
                    Color(
                        0.5 + ratio * (-0.32),
                        0.78 + ratio * (-0.29),
                        0.52 + ratio * (-0.32),
                        1,
                    )

                Rectangle(pos=(x, self.y), size=(bar_width, max(height, dp(3))))

    def set_week_data_from_stats(self, stats_data):
        weekly_minutes = stats_data.get("weekly_minutes", {})
        day_order = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        self.values = [weekly_minutes.get(day, 0) for day in day_order]
