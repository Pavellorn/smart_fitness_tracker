import json
import os


class StorageManager:

    def __init__(self):
        self.file_path = "backend_pavel/data/data.json"
        self.data = {}
        self.load()

    def _default_data(self):
        return {
            "current_workout": {
                "is_active": False,
                "selected_duration": None,
                "started_at": None,
                "paused_at": None,
                "elapsed_seconds": 0.0  # ← float
            },

            "stats": {
                "weekly_minutes": {
                    "mon": 0,
                    "tue": 0,
                    "wed": 0,
                    "thu": 0,
                    "fri": 0,
                    "sat": 0,
                    "sun": 0
                },
                "best_day": None,
                "total_week_minutes": 0
            },

            "settings": {
                "weekly_goal": 200,
                "notifications": True,
                "theme": "light"
            }
        }

    def load(self):

        if not os.path.exists(self.file_path):
            self.data = self._default_data()
            self.save()
            return

        try:
            with open(self.file_path, "r") as file:
                self.data = json.load(file)
        except (json.JSONDecodeError, FileNotFoundError):
            # защита от битого JSON
            self.data = self._default_data()
            self.save()

    def save(self):

        # гарантируем наличие папки
        os.makedirs(os.path.dirname(self.file_path), exist_ok=True)

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
            "elapsed_seconds": 0.0
        }

    def get_stats(self):
        return self.data["stats"]

    def update_stats(self, stats):
        self.data["stats"] = stats

    def get_settings(self):
        return self.data["settings"]

    def update_settings(self, settings):
        self.data["settings"] = settings