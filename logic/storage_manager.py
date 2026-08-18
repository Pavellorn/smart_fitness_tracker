"""Safe persistent storage for the fitness tracker."""

from __future__ import annotations

import json
import os
from copy import deepcopy
from pathlib import Path


class StorageManager:
    """Stores app state as UTF-8 JSON and keeps it compatible across releases."""

    DAYS = ("mon", "tue", "wed", "thu", "fri", "sat", "sun")

    def __init__(self, data_dir: str | os.PathLike[str] | None = None):
        project_dir = Path(__file__).resolve().parent.parent
        directory = Path(data_dir) if data_dir else project_dir / "data"
        directory.mkdir(parents=True, exist_ok=True)
        self.file_path = str(directory / "fitness_data.json")
        self.data: dict = {}
        self.load()

    def _default_data(self) -> dict:
        return {
            "current_workout": {
                "is_active": False,
                "selected_duration": None,
                "started_at": None,
                "paused_at": None,
                "elapsed_seconds": 0,
            },
            "stats": {
                "weekly_minutes": {day: 0 for day in self.DAYS},
                "best_day": None,
                "total_week_minutes": 0,
                "completed_workouts": 0,
                "total_sets": 0,
                "weekly_sets": {day: 0 for day in self.DAYS},
            },
            "settings": {"weekly_goal": 200, "notifications": True, "theme": "light"},
        }

    def _normalise(self, value: object) -> dict:
        """Merge older/incomplete files with defaults without losing valid data."""
        result = self._default_data()
        if not isinstance(value, dict):
            return result
        workout = value.get("current_workout", {})
        if isinstance(workout, dict):
            result["current_workout"].update(workout)
        stats = value.get("stats", {})
        if isinstance(stats, dict):
            weekly = stats.get("weekly_minutes", {})
            if isinstance(weekly, dict):
                result["stats"]["weekly_minutes"].update(
                    {day: max(0, int(weekly.get(day, 0) or 0)) for day in self.DAYS}
                )
            result["stats"].update({key: val for key, val in stats.items() if key != "weekly_minutes"})
        settings = value.get("settings", {})
        if isinstance(settings, dict):
            result["settings"].update(settings)
        result["stats"]["total_week_minutes"] = sum(result["stats"]["weekly_minutes"].values())
        if not isinstance(result["stats"].get("weekly_sets"), dict):
            result["stats"]["weekly_sets"] = {day: 0 for day in self.DAYS}
        result["stats"]["weekly_sets"] = {
            day: max(0, int(result["stats"]["weekly_sets"].get(day, 0) or 0))
            for day in self.DAYS
        }
        return result

    def load(self) -> None:
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                self.data = self._normalise(json.load(file))
        except (FileNotFoundError, json.JSONDecodeError, OSError):
            self.data = self._default_data()
            self.save()

    def save(self) -> None:
        """Write atomically so a killed mobile app cannot corrupt its state."""
        temp_path = f"{self.file_path}.tmp"
        with open(temp_path, "w", encoding="utf-8") as file:
            json.dump(self.data, file, ensure_ascii=False, indent=2)
        os.replace(temp_path, self.file_path)

    def get_current_workout(self):
        return self.data["current_workout"]

    def update_current_workout(self, workout):
        self.data["current_workout"] = deepcopy(workout)

    def reset_current_workout(self):
        self.data["current_workout"] = self._default_data()["current_workout"]

    def get_stats(self):
        return self.data["stats"]

    def update_stats(self, stats):
        self.data["stats"] = deepcopy(stats)

    def get_settings(self):
        return self.data["settings"]

    def update_settings(self, settings):
        self.data["settings"] = deepcopy(settings)
