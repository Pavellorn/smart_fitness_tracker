import json

import os

DATA_FILE = "fitness_data.json"


def load_data():
    """Загружаем данные из JSON"""
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r", encoding="utf-8") as file:
            return json.load(file)
    return get_default_data()


def save_data(data):
    """Сохраняем данные в JSON"""
    with open(DATA_FILE, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


def get_default_data():
    """Начальные данные"""

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
                "mon": 0,
                "tue": 0,
                "wed": 0,
                "thu": 0,
                "fri": 0,
                "sat": 0,
                "sun": 0,
            },
            "best_day": None,
            "total_week_minutes": 0,
        },
        "settings": {"weekly_goal": 200, "notifications": True, "theme": "light"},
    }


def reset_data():
    """Сброс всех данных"""
    data = get_default_data()
    save_data(data)
    return data
