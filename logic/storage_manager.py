import json
import os


class StorageManager:

    def __init__(self):
        # Получаем абсолютный путь. без этого ловил ошибки в нахождение fitness_data.json
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.file_path = os.path.join(base_dir, "data", "fitness_data.json")

        self.data = {}
        self.load()

    def _default_data(self):

        return {
            "current_workout": {
                "is_active": False,
                "selected_duration": None,
                "started_at": None,
                "paused_at": None,
                "elapsed_seconds": 0,
            },
            "stats": {
                "weekly_minutes": {
                    "mon": 200,
                    "tue": 0,
                    "wed": 0,
                    "thu": 0,
                    "fri": 0,
                    "sat": 555,
                    "sun": 0,
                },
                "best_day": None,
                "total_week_minutes": 0,
            },
            "settings": {"weekly_goal": 200, "notifications": True, "theme": "light"},
        }

    def load(self):

        if not os.path.exists(self.file_path):

            self.data = self._default_data()
            self.save()
            return

        with open(self.file_path, "r") as file:
            self.data = json.load(file)

    def save(self):

        with open(self.file_path, "w") as file:
            json.dump(self.data, file, indent=4)

    def get_current_workout(self):

        return self.data["current_workout"]

    def update_current_workout(self, workout):

        self.data["current_workout"] = workout

    def reset_current_workout(self):

        self.data["current_workout"] = {
            "is_active": False,
            "selected_duration": None,
            "started_at": None,
            "paused_at": None,
            "elapsed_seconds": 0,
        }

    def get_stats(self):

        return self.data["stats"]

    def update_stats(self, stats):

        self.data["stats"] = stats

    def get_settings(self):

        return self.data["settings"]

    def update_settings(self, settings):

        self.data["settings"] = settings
