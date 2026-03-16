# ======== ИМПОРТЫ =========
# Импортируем необходимые модули из библиотеки Kivy
from kivy.app import App  # Базовый класс для создания приложения
from kivy.uix.screenmanager import (
    ScreenManager,
    Screen,
    SlideTransition,
)  # Для управления экранами и переходами между ними
from kivy.uix.boxlayout import (
    BoxLayout,
)  # Контейнер, который располагает дочерние элементы в ряд или колонку
from kivy.uix.gridlayout import (
    GridLayout,
)  # Контейнер-сетка для расположения элементов в таблицу
from kivy.uix.label import Label  # Текстовые надписи
from kivy.uix.button import Button  # Кнопки
from kivy.uix.slider import Slider  # Ползунок для выбора значений
from kivy.uix.togglebutton import ToggleButton  # Кнопка-переключатель (вкл/выкл)
from kivy.animation import Animation  # Для создания анимаций
from kivy.graphics import (
    Color,
    Ellipse,
    Rectangle,
)  # Для рисования графических примитивов
from kivy.core.window import Window  # Для управления окном приложения

# Устанавливаем размер окна для разработки (ширина 400px, высота 700px)
Window.size = (400, 700)


# ========= ГРАДИЕНТНЫЙ ФОН =========
class GradientBackground(BoxLayout):
    """
    Класс для создания контейнера с градиентным фоном.
    Используется как основа для всех экранов приложения.
    """

    def __init__(self, **kwargs):
        # Вызываем конструктор родительского класса
        super().__init__(**kwargs)
        # Привязываем обновление фона к изменению размера или позиции виджета
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, *args):
        """
        Метод для отрисовки фона.
        Вызывается автоматически при изменении размеров виджета.
        """
        # Очищаем предыдущее содержимое canvas (область для рисования)
        self.canvas.before.clear()
        # Начинаем рисование на canvas
        with self.canvas.before:
            # Как в ТЗ цвет #f8f9fa
            Color(0.9725, 0.9765, 0.9804, 1)  # R, G, B, Alpha
            Rectangle(pos=self.pos, size=self.size)


# ========= АНИМИРОВАННЫЙ КРУГ =========
class AnimatedCircle(Button):
    """
    Класс для создания анимированной кнопки в виде круга.
    Отображает прогресс выполнения и пульсирующую анимацию.
    """

    def __init__(self, **kwargs):
        # Вызываем конструктор родительского класса
        super().__init__(**kwargs)
        # Делаем фон кнопки прозрачным (чтобы видеть нарисованный круг)
        self.background_color = (
            0,
            0,
            0,
            0,
        )  # R,G,B,A - все нули (полностью прозрачный)
        # Устанавливаем начальный текст
        self.text = "0 %"
        # Привязываем отрисовку круга к изменению позиции или размера
        self.bind(pos=self._draw, size=self._draw)

        # Создаем анимацию пульсации текста
        # Анимация увеличения размера шрифта
        anim_up = Animation(
            font_size=36, duration=0.3
        )  # Увеличиваем до 36 за 0.3 секунды
        # Анимация уменьшения размера шрифта
        anim_down = Animation(
            font_size=28, duration=0.3
        )  # Уменьшаем до 28 за 0.3 секунды
        # Объединяем анимации в последовательность (увеличение + уменьшение)
        self.anim = anim_up + anim_down
        # Устанавливаем повторение анимации
        self.anim.repeat = True
        # Запускаем анимацию
        self.anim.start(self)

    def _draw(self, *args):
        """
        Метод для отрисовки круга с индикацией прогресса.
        Рисует базовый круг и "заполненную" часть.
        """
        # Очищаем предыдущее содержимое canvas
        self.canvas.before.clear()
        # Начинаем рисование
        with self.canvas.before:
            # Рисуем базовый круг (фон)
            Color(0.2, 0.4, 0.6, 1)  # Синеватый цвет
            Ellipse(pos=self.pos, size=self.size)  # Эллипс, вписанный в размеры виджета

            # Рисуем "заполненную" часть (индикатор прогресса)
            Color(0.3, 0.9, 0.3, 1)  # Зеленый цвет
            # Рисуем только часть круга (имитация прогресса 50%)
            Ellipse(pos=self.pos, size=(self.width, self.height * 0.5))


# ========= ЭКРАН ТРЕНИРОВКИ =========
class TrainingScreen(Screen):
    """
    Главный экран приложения - экран тренировки.
    Содержит анимированный круг прогресса и кнопки выбора времени.
    """

    def __init__(self, **kwargs):
        # Вызываем конструктор родительского класса
        super().__init__(**kwargs)

        # Создаем корневой контейнер с градиентным фоном
        # orientation='vertical' - элементы располагаются вертикально
        # padding=20 - отступы от краев 20 пикселей
        # spacing=20 - расстояние между элементами 20 пикселей
        root = GradientBackground(orientation="vertical", padding=20, spacing=20)

        # Создаем и добавляем заголовок экрана
        # size_hint_y=0.1 - занимает 10% высоты родительского контейнера
        root.add_widget(
            Label(
                text="ТРЕНИРОВКА",
                font_size=32,
                color=(1, 1, 1, 1),
                bold=True,
                size_hint_y=0.1,
            )
        )

        # Создаем контейнер для анимированного круга
        circle_box = BoxLayout(size_hint_y=0.5)  # Занимает 50% высоты

        # Создаем анимированный круг
        # size_hint=(None, None) - отключаем автоматическое изменение размера
        # size=(200, 200) - устанавливаем фиксированный размер 200x200 пикселей
        circle = AnimatedCircle(size_hint=(None, None), size=(200, 200))
        # Центрируем круг по горизонтали
        circle.pos_hint = {"center_x": 0.5}  # 0.5 означает 50% от ширины родителя

        # Добавляем круг в контейнер
        circle_box.add_widget(circle)
        # Добавляем контейнер с кругом в корневой контейнер
        root.add_widget(circle_box)

        # Создаем контейнер для кнопок выбора времени тренировки
        buttons = BoxLayout(
            spacing=10, size_hint_y=0.2
        )  # Занимает 20% высоты, расстояние 10px между кнопками

        # Добавляем три кнопки с разным временем и цветами
        buttons.add_widget(
            Button(text="30 мин", background_color=(0.2, 0.8, 0.2, 1))
        )  # Зеленая
        buttons.add_widget(
            Button(text="60 мин", background_color=(1, 0.5, 0, 1))
        )  # Оранжевая
        buttons.add_widget(
            Button(text="90 мин", background_color=(0.8, 0.2, 0.2, 1))
        )  # Красная
        root.add_widget(buttons)

        # Создаем контейнер для навигационных стрелок
        arrows = BoxLayout(size_hint_y=0.1)  # Занимает 10% высоты

        # Создаем левую стрелку (переход к настройкам)
        left = Button(text="<--", font_size=30)
        # Привязываем событие нажатия к смене экрана
        # Используем setattr для изменения атрибута current менеджера экранов
        left.bind(on_press=lambda *_: setattr(self.manager, "current", "settings"))

        # Создаем правую стрелку (переход к статистике)
        right = Button(text="-->", font_size=30)
        right.bind(on_press=lambda *_: setattr(self.manager, "current", "stats"))

        # Добавляем стрелки в контейнер
        arrows.add_widget(left)
        arrows.add_widget(right)
        root.add_widget(arrows)

        # Добавляем корневой контейнер на экран
        self.add_widget(root)


# ========= ЭКРАН СТАТИСТИКИ =========
class StatsScreen(Screen):
    """
    Экран статистики активности за неделю.
    Отображает суммарное время и распределение по дням.
    """

    def __init__(self, **kwargs):
        # Вызываем конструктор родительского класса
        super().__init__(**kwargs)

        # Создаем корневой контейнер с градиентным фоном
        root = GradientBackground(orientation="vertical", padding=20, spacing=10)

        # Заголовок экрана статистики
        root.add_widget(
            Label(
                text="📊 ЗА НЕДЕЛЮ",
                font_size=28,
                color=(1, 1, 1, 1),
                bold=True,
                size_hint_y=0.1,
            )
        )

        # Отображение общего времени тренировок за неделю
        root.add_widget(
            Label(
                text="12ч 30мин 🏆",
                font_size=32,
                color=(1, 0.9, 0.2, 1),
                size_hint_y=0.1,
            )
        )

        # Создаем таблицу для отображения статистики по дням недели
        days = GridLayout(
            cols=7, size_hint_y=0.3
        )  # 7 колонок (по числу дней), 30% высоты

        # Названия дней недели
        names = ["Пн", "Вт", "Ср", "Чт", "Пт", "Сб", "Вс"]
        # Значения (количество тренировок или минут) для каждого дня
        vals = ["5", "12", "8", "15", "20", "18", "25"]

        # Создаем ячейки таблицы для каждого дня
        for n, v in zip(names, vals):
            # Для каждого дня создаем вертикальный контейнер
            box = BoxLayout(orientation="vertical")
            # Добавляем название дня
            box.add_widget(Label(text=n, font_size=14))
            # Добавляем значение
            box.add_widget(Label(text=v, font_size=14, color=(0.2, 0.8, 0.2, 1)))
            # Добавляем контейнер дня в таблицу
            days.add_widget(box)
        root.add_widget(days)

        # Отображение лучшего дня
        root.add_widget(
            Label(
                text="Лучший день: Пятница 20ч",
                font_size=16,
                color=(0.2, 0.8, 0.2, 1),
                size_hint_y=0.1,
            )
        )

        # Кнопка возврата на главный экран
        back = Button(
            text="← Назад",
            size_hint=(0.4, 0.1),  # 40% ширины, 10% высоты
            pos_hint={"center_x": 0.5},
        )  # Центрирование по горизонтали
        # Привязываем событие нажатия к смене экрана на главный
        back.bind(on_press=lambda *_: setattr(self.manager, "current", "main"))
        root.add_widget(back)

        # Добавляем корневой контейнер на экран
        self.add_widget(root)


# ========= ЭКРАН НАСТРОЕК =========
class SettingsScreen(Screen):
    """
    Экран настроек приложения.
    Позволяет настроить цель тренировок, уведомления и тему.
    """

    def __init__(self, **kwargs):
        # Вызываем конструктор родительского класса
        super().__init__(**kwargs)

        # Создаем корневой контейнер с градиентным фоном
        root = GradientBackground(orientation="vertical", padding=20, spacing=20)

        # Заголовок экрана настроек
        root.add_widget(
            Label(
                text="НАСТРОЙКИ",
                font_size=32,
                color=(1, 1, 1, 1),
                bold=True,
                size_hint_y=0.1,
            )
        )

        # Основной контейнер для элементов настроек
        box = BoxLayout(
            orientation="vertical", spacing=20, size_hint_y=0.6
        )  # 60% высоты

        # ----- НАСТРОЙКА ЦЕЛИ (слайдер) -----
        goal = BoxLayout(orientation="vertical")
        goal.add_widget(Label(text="Цель (мин/неделя):", font_size=18))
        # Слайдер для выбора значения от 100 до 500, начальное значение 300
        goal.add_widget(Slider(min=100, max=500, value=300))
        box.add_widget(goal)

        # ----- НАСТРОЙКА УВЕДОМЛЕНИЙ (переключатель) -----
        notify = BoxLayout(orientation="vertical")
        notify.add_widget(Label(text="Уведомления:", font_size=18))
        # ToggleButton - кнопка с двумя состояниями (нажата/отжата)
        # state='down' - изначально включена
        notify.add_widget(ToggleButton(text="ON", state="down"))
        box.add_widget(notify)

        # ----- НАСТРОЙКА ТЕМЫ (переключатель) -----
        theme = BoxLayout(orientation="vertical")
        theme.add_widget(Label(text="Тема:", font_size=18))
        theme.add_widget(ToggleButton(text="Тёмная"))  # По умолчанию выключена
        box.add_widget(theme)

        # Добавляем контейнер с настройками в корневой контейнер
        root.add_widget(box)

        # ----- КНОПКИ УПРАВЛЕНИЯ -----
        btns = BoxLayout(size_hint_y=0.15, spacing=10)  # 15% высоты
        btns.add_widget(
            Button(text="Сохранить", background_color=(0.2, 0.6, 0.2, 1))
        )  # Зеленая
        btns.add_widget(
            Button(text="Сбросить", background_color=(0.8, 0.2, 0.2, 1))
        )  # Красная
        root.add_widget(btns)

        # ----- КНОПКА ВОЗВРАТА -----
        back = Button(
            text="← Назад",
            size_hint=(0.4, 0.1),  # 40% ширины, 10% высоты
            pos_hint={"center_x": 0.5},
        )  # Центрирование
        # Привязываем событие нажатия к смене экрана на главный
        back.bind(on_press=lambda *_: setattr(self.manager, "current", "main"))
        root.add_widget(back)

        # Добавляем корневой контейнер на экран
        self.add_widget(root)


# ========= ГЛАВНОЕ ПРИЛОЖЕНИЕ =========
class UIApp(App):
    """
    Главный класс приложения.
    Управляет экранами и их переключением.
    """

    def build(self):
        """
        Метод build вызывается при запуске приложения.
        Должен возвращать корневой виджет приложения.
        """
        # Создаем менеджер экранов с анимацией перехода (скольжение)
        sm = ScreenManager(
            transition=SlideTransition(duration=0.3)
        )  # длительность 0.3 секунды

        # Добавляем экраны в менеджер с уникальными именами
        sm.add_widget(TrainingScreen(name="main"))  # Главный экран
        sm.add_widget(StatsScreen(name="stats"))  # Экран статистики
        sm.add_widget(SettingsScreen(name="settings"))  # Экран настроек

        # Возвращаем менеджер экранов как корневой виджет
        return sm


# ========= ТОЧКА ВХОДА =========
# Проверяем, запущен ли файл напрямую (не импортирован как модуль)
if __name__ == "__main__":
    # Создаем и запускаем приложение
    UIApp().run()
