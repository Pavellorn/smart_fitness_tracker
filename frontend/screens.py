from datetime import datetime
from kivy.clock import Clock
from kivy.animation import Animation
from kivy.properties import (
    StringProperty,
    NumericProperty,
    BooleanProperty,
    ListProperty,
)
from kivy.uix.screenmanager import Screen


class BaseFitnessScreen(Screen):
    """Базовый класс для страниц"""

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Добавляем атрибуты для бэкенда
        self.storage = None
        self.workout_manager = None
        self.stats_manager = None
        self.settings_manager = None

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
    """Страница тренировки"""

    timer_text = StringProperty("00:00")
    percent_text = StringProperty("0%")
    status_text = StringProperty("Выберите тренировку")
    progress_angle = NumericProperty(0)
    today_total_text = StringProperty("Сегодня: 0 мин")

    # Создаем свойство для цвета (изначально зеленый)
    circle_color = ListProperty([0.298, 0.686, 0.314, 1])

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        self.timer_event = None
        self.current_workout_duration = 0

    def on_progress_angle(self, instance, value):
        # value — это угол от 0 до 360
        if value < 120:  # Первая треть
            self.circle_color = [0.298, 0.686, 0.314, 1]  # Зеленый
        elif value < 240:  # Вторая треть
            self.circle_color = [1.0, 0.596, 0.0, 1]  # Оранжевый
        else:  # Финал
            self.circle_color = [0.85, 0.3, 0.3, 1]  # Красный

    def on_enter(self):
        """Обновление при входе на экран"""
        self.update_today_stats()
        self.restore_workout()

    def update_today_stats(self):
        """Обновление статистики за сегодня"""
        if self.stats_manager:
            stats = self.stats_manager.storage.get_stats()
            day_key = self.stats_manager._get_today()
            mins = stats["weekly_minutes"].get(day_key, 0)
            self.today_total_text = f"Сегодня: {int(mins)} мин"

    def restore_workout(self):
        """Восстановить незавершенную тренировку"""
        if self.workout_manager and self.workout_manager.is_active():
            current = self.workout_manager.storage.get_current_workout()
            self.current_workout_duration = current.get("selected_duration", 0)

            if self.workout_manager.is_paused():
                self.status_text = "Тренировка на паузе"
                self.update_timer_display(current.get("elapsed_seconds", 0))
            else:
                self.status_text = "Тренировка продолжается"
                self.start_timer()
                self.start_heart_beat()  

    def start_workout(self, minutes):
        """Инициализация и запуск таймера тренировки"""
        if not self.workout_manager:
            self.show_status("Ошибка: бэкенд не подключен")
            return

        # Используем готовый метод бэкенда
        self.workout_manager.start(minutes)
        self.current_workout_duration = minutes
        self.status_text = f"Тренировка {minutes} минут"
        self.start_timer()

    def start_timer(self):
        """Запуск обновления таймера"""
        if self.timer_event:
            self.timer_event.cancel()
        self.timer_event = Clock.schedule_interval(self.update_timer, 1)

    def update_timer(self, dt):
        """Обновление таймера каждую секунду"""
        if not self.workout_manager:
            return False

        # Используем метод бэкенда для расчета
        current = self.workout_manager.storage.get_current_workout()
        elapsed = self.workout_manager._calculate_total_elapsed(current)
        total_seconds = self.current_workout_duration * 60

        # Форматируем время
        minutes = elapsed // 60
        seconds = elapsed % 60
        self.timer_text = f"{minutes:02d}:{seconds:02d}"

        # Обновляем прогресс
        if total_seconds > 0:
            percent = (elapsed / total_seconds) * 100
            self.progress_angle = (percent / 100) * 360
            self.percent_text = f"{int(percent)}%"

        # Проверяем завершение через бэкенд
        if self.workout_manager.get_remaining_seconds() <= 0:
            self.finish_workout()
            return False

        return True

    def update_timer_display(self, elapsed_seconds):
        """Обновить отображение таймера без запуска обновления"""
        minutes = elapsed_seconds // 60
        seconds = elapsed_seconds % 60
        self.timer_text = f"{minutes:02d}:{seconds:02d}"

        total_seconds = self.current_workout_duration * 60
        if total_seconds > 0:
            percent = (elapsed_seconds / total_seconds) * 100
            self.progress_angle = (percent / 100) * 360
            self.percent_text = f"{int(percent)}%"

    def pause_workout(self):
        """Приостановка текущего таймера"""
        if self.workout_manager:
            self.workout_manager.pause()
            if self.timer_event:
                self.timer_event.cancel()
            self.status_text = "Тренировка на паузе"
            self.stop_heart_beat()
            
    def resume_workout(self):
        """Возобновление работы таймера"""
        if self.workout_manager:
            self.workout_manager.resume()
            self.status_text = "Тренировка продолжается"
            self.start_timer()
            self.start_heart_beat()
            
    def cancel_workout(self):
        """Полный сброс текущей тренировки"""
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        if self.workout_manager:
            # Сбрасываем через storage напрямую
            self.workout_manager.storage.reset_current_workout()
            self.workout_manager.storage.save()

        # Сбрасываем отображение
        self.timer_text = "00:00"
        self.progress_angle = 0
        self.percent_text = "0%"
        self.status_text = "Тренировка отменена"
        self.update_today_stats()

        self.stop_heart_beat()
        
    def finish_workout(self):
        """Завершение тренировки"""
        if self.timer_event:
            self.timer_event.cancel()
            self.timer_event = None

        if self.workout_manager:
            self.workout_manager.finish()

        self.status_text = "Тренировка завершена!"
        self.show_status("Отлично! Тренировка завершена")
        self.update_today_stats()

        self.stop_heart_beat()
        
        # Планируем сброс статуса через 3 секунды
        Clock.schedule_once(lambda dt: self.reset_status(), 3)

        
    def reset_status(self):
        """Сброс статуса после завершения"""
        self.status_text = "Выберите тренировку"
        self.timer_text = "00:00"
        self.progress_angle = 0
        self.percent_text = "0%"
        
        
#ТУТ НАСТРОЙКИ СЕРДЦА
    def start_heart_beat(self):
        """Запускает биение сердца (увеличивается и уменьшается)"""
        heart = self.ids.heart_icon
        Animation.cancel_all(heart)
        
        # Увеличить → уменьшить → повторять
        anim = Animation(font_size=240, duration=0.3) + \
               Animation(font_size=200, duration=0.3)
        anim.repeat = True
        anim.start(heart)
    
    def stop_heart_beat(self):
        """Останавливает биение"""
        heart = self.ids.heart_icon
        Animation.cancel_all(heart)
        
        heart.font_size = 200  # Возвращаем как было
    
class StatsScreen(BaseFitnessScreen):
    total_text = StringProperty("0ч 0мин")
    graph_values = ListProperty([0] * 7)
    goal_progress_text = StringProperty("0%")
    remaining_text = StringProperty("Осталось: 0 мин")

    def on_enter(self):
        """Обновление статистики при входе на экран"""
        self.update_stats()

    def update_stats(self):
        """Обновление всех статистических данных"""
        if not self.stats_manager:
            return

        # Получаем данные через stats_manager
        stats = self.stats_manager.storage.get_stats()
        weekly = stats["weekly_minutes"]
        settings = self.stats_manager.storage.get_settings()
        goal = settings.get("weekly_goal", 200)

        # Формируем данные для графика
        days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        self.graph_values = [weekly.get(d, 0) for d in days]

        # Рассчитываем общее время
        total = sum(self.graph_values)
        hours = int(total // 60)
        minutes = int(total % 60)
        self.total_text = f"{hours}ч {minutes}мин"

        # Рассчитываем прогресс к цели
        if goal > 0:
            progress_percent = int((total / goal) * 100)
            self.goal_progress_text = f"{progress_percent}%"
            remaining = max(0, goal - total)
            self.remaining_text = f"Осталось: {int(remaining)} мин"
        else:
            self.goal_progress_text = "0%"
            self.remaining_text = "Цель не установлена"

        # Обновляем график
        if "week_graph" in self.ids:
            self.ids.week_graph.values = self.graph_values

    def reset_week(self):
        """Сброс статистики за неделю"""
        if self.stats_manager:
            # Сбрасываем через storage
            stats = self.stats_manager.storage.get_stats()
            stats["weekly_minutes"] = {
                d: 0 for d in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
            }
            self.stats_manager.storage.update_stats(stats)
            self.stats_manager.storage.save()
            self.update_stats()
            self.show_status("Статистика сброшена")


class SettingsScreen(BaseFitnessScreen):
    goal_value = NumericProperty(200)
    goal_text = StringProperty("")
    notif_state = BooleanProperty(True)

    def on_enter(self):
        """Загрузка настроек при входе на экран"""
        self.load_settings()

    def load_settings(self):
        """Загрузка настроек из бэкенда"""
        if not self.settings_manager:
            return

        settings = self.settings_manager.storage.get_settings()
        self.goal_value = settings.get("weekly_goal", 200)
        self.notif_state = settings.get("notifications", True)
        self.goal_text = f"{int(self.goal_value)} мин/неделю"

    def on_goal_change(self, value, instance=None):
        """Обработка изменения цели"""
        self.goal_value = value
        self.goal_text = f"{int(value)} мин/неделю"

    def save_current_settings(self):
        """Сохранение текущих настроек"""
        if not self.settings_manager:
            return

        # Сохраняем через settings_manager
        settings = self.settings_manager.storage.get_settings()
        settings["weekly_goal"] = int(self.goal_value)
        settings["notifications"] = self.notif_state
        self.settings_manager.storage.update_settings(settings)
        self.settings_manager.storage.save()

        self.show_status("Сохранено!")

    def reset_settings(self):
        """Сброс настроек к значениям по умолчанию"""
        if self.settings_manager:
            default = {"weekly_goal": 200, "notifications": True, "theme": "light"}
            self.settings_manager.storage.update_settings(default)
            self.settings_manager.storage.save()
            self.load_settings()
            self.show_status("Сброшено")

    def toggle_notifications(self):
        """Переключение уведомлений"""
        self.notif_state = not self.notif_state
        self.save_current_settings()

    def reset_week_only(self):
        """Сброс только недельной статистики (для кнопки в настройках)"""
        if self.stats_manager:
            self.stats_manager.storage.get_stats()["weekly_minutes"] = {
                d: 0 for d in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
            }
            self.stats_manager.storage.save()
            self.show_status("Неделя сброшена")
