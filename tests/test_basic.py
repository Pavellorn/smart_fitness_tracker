"""
Базовые тесты для бэкенд-логики фитнес-приложения.
Запуск из корня проекта: pytest tests/test_basic.py -v
"""

import os
import sys
import json
import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta

# ====== ФИКС ПУТЕЙ ======
# Добавляем корень проекта (папку выше tests/) в sys.path,
# чтобы Python нашёл модули logic и frontend
sys.path.insert(0, os.path.join(os.path.dirname(__file__), ".."))

from logic.storage_manager import StorageManager
from logic.workout_manager import WorkoutManager


# --- Фикстуры ---

@pytest.fixture
def tmp_storage(tmp_path):
    """
    Создаёт StorageManager с временным файлом,
    чтобы тесты не трогали реальные данные.
    """
    storage = StorageManager.__new__(StorageManager)
    storage.file_path = str(tmp_path / "test_data.json")
    storage.data = storage._default_data()
    storage.save()
    return storage


@pytest.fixture
def stats_manager_mock():
    """Мок StatsManager — проверяем что workout_manager его вызывает."""
    mock = MagicMock()
    mock.add_workout = MagicMock()
    return mock


@pytest.fixture
def workout_mgr(tmp_storage, stats_manager_mock):
    """WorkoutManager с подставным storage и stats."""
    return WorkoutManager(tmp_storage, stats_manager_mock)


# ============================================================
# ТЕСТЫ StorageManager
# ============================================================

class TestStorageManager:

    def test_default_data_structure(self, tmp_storage):
        """Дефолтные данные содержат все нужные ключи."""
        data = tmp_storage.data
        assert "current_workout" in data
        assert "stats" in data
        assert "settings" in data
        assert len(data["stats"]["weekly_minutes"]) == 7

    def test_save_and_load(self, tmp_storage):
        """Данные сохраняются в файл и читаются обратно."""
        tmp_storage.data["settings"]["weekly_goal"] = 999
        tmp_storage.save()

        with open(tmp_storage.file_path) as f:
            raw = json.load(f)
        assert raw["settings"]["weekly_goal"] == 999

    def test_get_and_update_settings(self, tmp_storage):
        """Геттер и сеттер настроек работают согласованно."""
        new_settings = {"weekly_goal": 300, "notifications": False, "theme": "dark"}
        tmp_storage.update_settings(new_settings)

        result = tmp_storage.get_settings()
        assert result["weekly_goal"] == 300
        assert result["notifications"] is False

    def test_reset_current_workout(self, tmp_storage):
        """После сброса тренировка неактивна и поля обнулены."""
        tmp_storage.data["current_workout"]["is_active"] = True
        tmp_storage.data["current_workout"]["selected_duration"] = 30

        tmp_storage.reset_current_workout()
        w = tmp_storage.get_current_workout()

        assert w["is_active"] is False
        assert w["selected_duration"] is None
        assert w["elapsed_seconds"] == 0


# ============================================================
# ТЕСТЫ WorkoutManager
# ============================================================

class TestWorkoutManager:

    def test_start_creates_active_workout(self, workout_mgr, tmp_storage):
        """После start() тренировка активна."""
        workout_mgr.start(30)

        current = tmp_storage.get_current_workout()
        assert current["is_active"] is True
        assert current["selected_duration"] == 30
        assert current["started_at"] is not None

    def test_start_ignores_if_already_active(self, workout_mgr, tmp_storage):
        """Повторный start() не перезаписывает текущую тренировку."""
        workout_mgr.start(30)
        first_start = tmp_storage.get_current_workout()["started_at"]

        workout_mgr.start(60)
        second_start = tmp_storage.get_current_workout()["started_at"]

        assert first_start == second_start
        assert tmp_storage.get_current_workout()["selected_duration"] == 30
