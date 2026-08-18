# Smart Fitness

Кроссплатформенный трекер тренировок на Python и Kivy. Один код запускается на Windows/Linux/macOS и собирается в Android-приложение.

## Что умеет

- таймер тренировки на 30, 60 или 90 минут с паузой, продолжением и отменой;
- сохранение незавершённой тренировки после перезапуска;
- недельная статистика, график активности и прогресс к цели;
- настройка недельной цели, уведомлений и светлой/тёмной темы;
- надёжное JSON-хранилище: миграция старых данных, UTF-8 и атомарная запись.

## Запуск на компьютере

```bash
uv sync
uv run python main.py
```

Проверка логики:

```bash
uv run --group dev pytest -q
```

## Android (APK)

Конфигурация уже находится в `buildozer.spec`. Собирать APK нужно в Linux или WSL2 — Buildozer не поддерживает нативную сборку в Windows.

```bash
sudo apt update
sudo apt install -y git zip unzip openjdk-17-jdk python3-pip
python3 -m pip install --user buildozer cython
buildozer android debug
```

Готовый установочный файл появится в `bin/`. Для установки на подключённый телефон с включённой USB-отладкой:

```bash
buildozer android deploy run
```

На Android данные сохраняются в личной директории приложения (`App.user_data_dir`), поэтому обновление интерфейса не затирает историю тренировок.
