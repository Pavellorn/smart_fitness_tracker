from datetime import datetime


class WorkoutManager:

    def __init__(self, storage, stats_manager):
        self.storage = storage
        self.stats_manager = stats_manager

    def _get_now(self):
        return datetime.now()

    def _current(self):
        return self.storage.get_current_workout()

    def start(self, duration: int):
        current = self._current()

        if current["is_active"]:
            return

        now = self._get_now()

        current["is_active"] = True
        current["selected_duration"] = duration
        current["started_at"] = now.isoformat()
        current["paused_at"] = None
        current["elapsed_seconds"] = 0.0  # ← float

        self.storage.update_current_workout(current)
        self.storage.save()

    def pause(self):
        current = self._current()

        if not current["is_active"]:
            return

        if current["paused_at"] is not None:
            return

        if not current["started_at"]:
            return

        now = self._get_now()
        started_at = datetime.fromisoformat(current["started_at"])

        elapsed = (now - started_at).total_seconds()
        current["elapsed_seconds"] += elapsed  # ← без int

        current["paused_at"] = now.isoformat()

        self.storage.update_current_workout(current)
        self.storage.save()

    def resume(self):
        current = self._current()

        if not current["is_active"]:
            return

        if current["paused_at"] is None:
            return

        now = self._get_now()

        current["started_at"] = now.isoformat()
        current["paused_at"] = None

        self.storage.update_current_workout(current)
        self.storage.save()

    def finish(self):
        current = self._current()

        if not current["is_active"]:
            return

        total_elapsed = self._calculate_total_elapsed(current)

        minutes = int(total_elapsed // 60)

        if minutes > 0:
            self.stats_manager.add_workout(minutes)

        self.storage.reset_current_workout()
        self.storage.save()

    def _calculate_total_elapsed(self, current):
        elapsed = current["elapsed_seconds"]

        if current["paused_at"] is None and current["started_at"]:
            now = self._get_now()
            started_at = datetime.fromisoformat(current["started_at"])
            elapsed += (now - started_at).total_seconds()

        return elapsed

    def get_remaining_seconds(self):
        current = self._current()

        if not current["is_active"]:
            return 0

        duration_seconds = current["selected_duration"] * 60
        elapsed = self._calculate_total_elapsed(current)

        remaining = max(0, int(duration_seconds - elapsed))

        return remaining

    def is_active(self):
        return self._current()["is_active"]

    def is_paused(self):
        return self._current()["paused_at"] is not None

    def resume_if_needed(self):
        current = self._current()

        if not current["is_active"]:
            return

        if current["paused_at"] is not None:
            return

        duration_seconds = current["selected_duration"] * 60

        if self._calculate_total_elapsed(current) >= duration_seconds:
            self.finish()
            return