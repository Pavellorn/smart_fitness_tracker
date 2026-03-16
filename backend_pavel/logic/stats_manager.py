from datetime import datetime


class StatsManager:
    def __init__(self, storage):
        self.storage = storage

    def add_workout(self, minutes):
        stats = self.storage.get_stats()
        day = self._get_today()
        stats["weekly_minutes"][day] += minutes
        stats["total_week_minutes"] = sum(stats["weekly_minutes"].values())
        stats["best_day"] = self._calculate_best_day(stats["weekly_minutes"])
        self.storage.update_stats(stats)
        self.storage.save()

    def _get_today(self):
        weekday = datetime.now().weekday()
        days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]
        return days[weekday]

    def _calculate_best_day(self, weekly_minutes):
        if max(weekly_minutes.values()) == 0:
            return None
        return max(weekly_minutes, key=weekly_minutes.get)
