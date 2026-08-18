from datetime import datetime


class StatsManager:

    def __init__(self, storage):

        self.storage = storage


    def add_workout(self, minutes):
        minutes = max(0, int(minutes))
        if not minutes:
            return
        stats = self.storage.get_stats()

        day = self._get_today()

        stats["weekly_minutes"][day] += minutes

        stats["total_week_minutes"] = sum(stats["weekly_minutes"].values())

        stats["best_day"] = self._calculate_best_day(stats["weekly_minutes"])
        stats["completed_workouts"] = int(stats.get("completed_workouts", 0)) + 1

        self.storage.update_stats(stats)

        self.storage.save()

    def add_set(self):
        """Record one completed strength-training set for the current weekday."""
        stats = self.storage.get_stats()
        day = self._get_today()
        stats.setdefault("weekly_sets", {name: 0 for name in ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]})
        stats["weekly_sets"][day] = int(stats["weekly_sets"].get(day, 0)) + 1
        stats["total_sets"] = int(stats.get("total_sets", 0)) + 1
        self.storage.update_stats(stats)
        self.storage.save()


    def _get_today(self):

        weekday = datetime.now().weekday()

        days = ["mon", "tue", "wed", "thu", "fri", "sat", "sun"]

        return days[weekday]


    def _calculate_best_day(self, weekly_minutes):

        return max(weekly_minutes, key=weekly_minutes.get)
