"""
Экран статистики.
Отображает активность за неделю.
"""

from kivy.uix.screenmanager import Screen
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.gridlayout import GridLayout
from kivy.uix.label import Label
from kivy.uix.button import Button

from kv.background import Background
from utils.constants import COLORS, WEEKDAYS


class StatsScreen(Screen):
    """
    Экран статистики активности за неделю.
    """

    def __init__(self, **kwargs):
        super().__init__(**kwargs)

        root = Background(orientation="vertical", padding=20, spacing=10)

        # Заголовок
        root.add_widget(
            Label(
                text="📊 ЗА НЕДЕЛЮ",
                font_size=28,
                color=COLORS["white"],
                bold=True,
                size_hint_y=0.1,
            )
        )

        # Общее время
        root.add_widget(
            Label(
                text="12ч 30мин 🏆",
                font_size=32,
                color=COLORS["accent"],
                size_hint_y=0.1,
            )
        )

        # Таблица дней
        days = GridLayout(cols=7, size_hint_y=0.3)
        values = ["5", "12", "8", "15", "20", "18", "25"]

        for day_name, day_value in zip(WEEKDAYS, values):
            box = BoxLayout(orientation="vertical")
            box.add_widget(Label(text=day_name, font_size=14))
            box.add_widget(Label(text=day_value, font_size=14, color=COLORS["success"]))
            days.add_widget(box)
        root.add_widget(days)

        # Лучший день
        root.add_widget(
            Label(
                text="Лучший день: Пятница 20ч",
                font_size=16,
                color=COLORS["success"],
                size_hint_y=0.1,
            )
        )

        # Кнопка возврата
        back = Button(text="← Назад", size_hint=(0.4, 0.1), pos_hint={"center_x": 0.5})
        back.bind(on_press=lambda x: self.go_to_main())
        root.add_widget(back)

        self.add_widget(root)

    def go_to_main(self):
        """Переход на главный экран."""
        self.manager.current = "main"
