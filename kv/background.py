"""
Класс для создания контейнера с однотонным фоном.
Используется как основа для всех экранов приложения.
"""

from kivy.uix.boxlayout import BoxLayout
from kivy.graphics import Color, Rectangle
from utils.constants import COLORS


class Background(BoxLayout):
    """
    Контейнер с однотонным фоном.
    Автоматически обновляет фон при изменении размера.
    """
    
    def __init__(self, **kwargs):
        """
        Инициализация фона.
        Args:
            **kwargs: Параметры для BoxLayout (orientation, padding, spacing)
        """
        super().__init__(**kwargs)
        self.bind(size=self._update_bg, pos=self._update_bg)

    def _update_bg(self, *args):
        """
        Отрисовка фона.
        Вызывается при изменении размеров виджета.
        """
        self.canvas.before.clear()
        with self.canvas.before:
            Color(*COLORS['text']) # тут просто образаемся по ключу и распаковываем значения 
            Rectangle(pos=self.pos, size=self.size)