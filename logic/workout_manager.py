from datetime import datetime


class WorkoutManager:
    """State machine for a workout timer, independent from the Kivy interface."""

    def __init__(self, storage, stats_manager):
        self.storage = storage
        self.stats_manager = stats_manager

    def _get_now(self):
        return datetime.now()

    def start(self, duration: int) -> bool:
        if not isinstance(duration, int) or duration <= 0:
            raise ValueError("Workout duration must be a positive integer")
        current = self.storage.get_current_workout()
        if current["is_active"]:
            return False
        current.update({"is_active": True, "selected_duration": duration,
                        "started_at": self._get_now().isoformat(), "paused_at": None,
                        "elapsed_seconds": 0})
        self.storage.update_current_workout(current)
        self.storage.save()
        return True

    def _current(self):
        return self.storage.get_current_workout()

    def pause(self) -> bool:
        current = self._current()
        if not current.get("is_active") or current.get("paused_at") is not None:
            return False
        current["elapsed_seconds"] = self._calculate_total_elapsed(current)
        current["paused_at"] = self._get_now().isoformat()
        self.storage.update_current_workout(current)
        self.storage.save()
        return True

    def resume(self) -> bool:
        current = self._current()
        if not current.get("is_active") or current.get("paused_at") is None:
            return False
        current["started_at"] = self._get_now().isoformat()
        current["paused_at"] = None
        self.storage.update_current_workout(current)
        self.storage.save()
        return True

    def cancel(self) -> bool:
        if not self._current().get("is_active"):
            return False
        self.storage.reset_current_workout()
        self.storage.save()
        return True

    def finish(self) -> int:
        current = self._current()
        if not current.get("is_active") or not current.get("selected_duration"):
            return 0
        minutes = self._calculate_total_elapsed(current) // 60
        if minutes:
            self.stats_manager.add_workout(minutes)
        self.storage.reset_current_workout()
        self.storage.save()
        return minutes

    def _calculate_total_elapsed(self, current) -> int:
        elapsed = max(0, int(current.get("elapsed_seconds", 0) or 0))
        if current.get("paused_at") is None and current.get("started_at"):
            started_at = datetime.fromisoformat(current["started_at"])
            elapsed += max(0, int((self._get_now() - started_at).total_seconds()))
        return elapsed

    def get_remaining_seconds(self) -> int:
        current = self._current()
        duration = current.get("selected_duration")
        if not current.get("is_active") or duration is None:
            return 0
        return max(0, int(duration) * 60 - self._calculate_total_elapsed(current))

    def is_active(self):
        return bool(self._current().get("is_active"))

    def is_paused(self):
        return self._current().get("paused_at") is not None

    def add_set(self, exercise: str, weight: float, reps: int) -> dict:
        """Append a completed strength set to the active local workout."""
        exercise = exercise.strip()
        if not exercise or weight < 0 or reps <= 0:
            raise ValueError("Exercise, non-negative weight and positive repetitions are required")
        current = self._current()
        current.setdefault("sets", [])
        record = {"exercise": exercise, "weight": round(float(weight), 1), "reps": int(reps)}
        current["sets"].append(record)
        current["is_active"] = True
        self.storage.update_current_workout(current)
        self.storage.save()
        self.stats_manager.add_set()
        return record
