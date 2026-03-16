from datetime import datetime


class WorkoutManager:
    def __init__(self, storage, stats_manager):
        self.storage = storage
        self.stats_manager = stats_manager

    def _get_now(self):
        return datetime.now()

    def start(self, duration: int):
        current = self.storage.get_current_workout()
        if current["is_active"]:
            return

        current["is_active"] = True
        current["selected_duration"] = duration
        current["started_at"] = self._get_now().isoformat()
        current["paused_at"] = None
        current["elapsed_seconds"] = 0

        self.storage.update_current_workout(current)
        self.storage.save()

    def _current(self):
        return self.storage.get_current_workout()

    def pause(self):
        current = self._current()
        if not current["is_active"]:
            return
        if current["paused_at"] is not None:
            return
        started_at = datetime.fromisoformat(current["started_at"])
        elapsed = (self._get_now() - started_at).total_seconds() # прошло времени
        current["elapsed_seconds"] += int(elapsed)
        current["paused_at"] = self._get_now().isoformat()
        self.storage.update_current_workout(current)
        self.storage.save()

    def resume(self):
        current = self._current()
        if not current["is_active"]:
            return
        if current["paused_at"] is None:
            return
        current["started_at"] = self._get_now().isoformat()
        current["paused_at"] = None

        self.storage.update_current_workout(current)
        self.storage.save()

    def finish(self):
        current = self._current()
        if not current["is_active"]:
            return
        total_elapsed = self._calculate_total_elapsed(current) # всего прошло
        minutes = total_elapsed // 60
        if minutes > 0:
            self.stats_manager.add_workout(minutes)
        self.storage.reset_current_workout()
        self.storage.save()

    def _calculate_total_elapsed(self, current):
        elapsed = current["elapsed_seconds"]
        if current["paused_at"] is None:
            started_at = datetime.fromisoformat(current["started_at"])
            elapsed += int((self._get_now() - started_at).total_seconds())
        return elapsed

    def get_remaining_seconds(self):
        current = self._current()
        if not current["is_active"]:
            return 0
        duration_seconds = current["selected_duration"] * 60
        elapsed = self._calculate_total_elapsed(current)
        remaining = duration_seconds - elapsed
        return max(0, remaining)

    def is_active(self):
        current = self._current()
        return current["is_active"]

    def is_paused(self):
        current = self.storage.get_current_workout()
        return current["paused_at"] is not None
    
    def resume_if_needed(self):
        current = self._current()
        if not current["is_active"]:
            return
            
        if current["paused_at"] is not None:
            return
            
        if self._calculate_total_elapsed(current) >= current["selected_duration"] * 60:
             self.finish()
