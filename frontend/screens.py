from datetime import datetime
from kivy.clock import Clock
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ListProperty,
)
from kivy.uix.screenmanager import Screen

from backend.storage import (
    load_data,
    save_data,
)


class BaseFitnessScreen(Screen):
    """Базовый класс для страниц"""

    txt_color = ListProperty([0.173, 0.243, 0.314, 1])
    bg_color = ListProperty([0.97, 0.98, 0.98, 1])

    def go_to(self, screen_name):
        sm = self.manager
        screens = ["workout", "stats", "settings"]
        sm.transition.direction = (
            "left"
            if screens.index(screen_name) > screens.index(sm.current)
            else "right"
        )
        sm.current = screen_name

    def toggle_theme(self):
        if self.bg_color == [0.973, 0.976, 0.980, 1]:
            new_bg, new_txt = [0.1, 0.1, 0.12, 1], [0.95, 0.95, 0.97, 1]
        else:
            new_bg, new_txt = [0.973, 0.976, 0.980, 1], [0.173, 0.243, 0.314, 1]
        for screen in self.manager.screens:
            screen.bg_color = new_bg
            screen.txt_color = new_txt

    def show_status(self, text):
        if "save_status" in self.ids:
            self.ids.save_status.text = text
            Clock.schedule_once(lambda dt: setattr(self.ids.save_status, "text", ""), 2)


class WorkoutScreen(BaseFitnessScreen):
    """Страницу с методами запуска тренировки
    и отображения анимированного круга нужно реализовать!!!!"""

    timer_text = StringProperty("00:00")
    percent_text = StringProperty("0%")
    status_text = StringProperty("Выберите тренировку")
    progress_angle = NumericProperty(0)
    today_total_text = StringProperty("Сегодня: 0 мин")

    def on_enter(self):
        """Обновление общей статистики"""
        data = load_data()
        day_key = datetime.now().strftime("%a").lower()
        mins = data["stats"]["weekly_minutes"].get(day_key, 0)
        self.today_total_text = f"Сегодня: {int(mins)} мин"

    def restore_workout(self):
        """Восстановить тренировку"""
        pass

    def start_workout(self, minutes):
        """Инициализация и запуск таймера тренировки"""
        pass

    def pause_workout(self):
        """Приостановка текущего таймера и анимации"""
        pass

    def resume_workout(self):
        """Возобновление работы таймера и анимации"""
        pass

    def stop_all(self):
        """Принудительная остановка все что происходит на экране"""
        pass

    def cancel_workout(self):
        """Полный сброс текущей тренировки (вызывается из KV)root.cancel_()"""
        pass


class StatsScreen(BaseFitnessScreen):
    total_text = StringProperty("0ч 0мин")
    graph_values = ListProperty([0] * 7)
    goal_progress_text = StringProperty("0%")
    remaining_text = StringProperty("Осталось: 0 мин")

    def on_enter(self):
        data = load_data()
        stats = data.get("stats", {}).get("weekly_minutes", {})
        goal = data.get("settings", {}).get("weekly_goal", 200)
        days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        self.graph_values = [stats.get(d, 0) for d in days]
        total = sum(self.graph_values)
        self.total_text = f"{int(total//60)}ч {int(total%60)}мин"
        self.goal_progress_text = f"{int((total/goal)*100 if goal > 0 else 0)}%"
        self.remaining_text = f"Осталось: {max(0, int(goal-total))} мин"
        if "week_graph" in self.ids:
            self.ids.week_graph.values = self.graph_values

    def reset_week(self):
        data = load_data()
        data["stats"]["weekly_minutes"] = {
            d: 0 for d in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        }
        save_data(data)
        self.on_enter()


class SettingsScreen(BaseFitnessScreen):
    goal_value = NumericProperty(200)
    goal_text = StringProperty("")
    notif_state = BooleanProperty(True)

    def on_enter(self):
        data = load_data().get("settings", {})
        self.goal_value = data.get("weekly_goal", 200)
        self.notif_state = data.get("notifications", True)
        self.goal_text = f"{int(self.goal_value)} мин/неделю"

    def on_goal_change(self, value, instance=None):
        self.goal_value = value
        self.goal_text = f"{int(value)} мин/неделю"

    def save_current_settings(self):
        data = load_data()
        data["settings"]["weekly_goal"] = int(self.goal_value)
        data["settings"]["notifications"] = self.notif_state
        save_data(data)
        self.show_status("Сохранено!")

    def reset_settings(self):
        data = load_data()
        data["settings"] = {"weekly_goal": 200, "notifications": True, "theme": "light"}
        save_data(data)
        self.on_enter()
        self.show_status("Сброшено")

    def toggle_notifications(self):
        self.notif_state = not self.notif_state
